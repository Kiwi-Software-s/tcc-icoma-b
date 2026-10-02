import functools

from flask import Blueprint, current_app, jsonify, redirect, render_template, request, session, url_for
from firebase_admin import auth as firebase_auth

from app.firebase_config import init_firebase
from app.repositories.user_repository import garantir_usuario, obter_tipo_usuario


auth_bp = Blueprint("auth", __name__)


def login_required(view):
    """Decorator que protege rotas exigindo uma sessão autenticada."""
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        uid = session.get("uid")
        if not uid:
            return redirect(url_for("auth.login"))

        # Mantém a permissão da sessão sincronizada com o Firestore.
        # Assim, quando um admin promove/rebaixa uma conta, o menu correto
        # aparece já na próxima página protegida, sem precisar sair e entrar.
        try:
            session["tipo"] = obter_tipo_usuario(uid)
        except Exception as exc:
            # Falha de rede não deve derrubar a navegação. Mantém o último
            # papel conhecido da sessão e as rotas sensíveis continuam
            # validando novamente a permissão no backend.
            print(f"Não foi possível atualizar o tipo do usuário: {type(exc).__name__}")
            session.setdefault("tipo", "usuario")

        return view(*args, **kwargs)
    return wrapped_view


@auth_bp.route("/login")
def login():
    if session.get("uid"):
        return redirect(url_for("home.dashboard"))
    return render_template("login/login.html")


@auth_bp.route("/cadastro")
def cadastro():
    if session.get("uid"):
        return redirect(url_for("home.dashboard"))
    return render_template("login/register.html")


@auth_bp.route("/auth/session", methods=["POST"])
def criar_sessao():
    """Valida o idToken do Firebase e cria a sessão Flask."""
    data = request.get_json(silent=True)
    id_token = data.get("idToken") if isinstance(data, dict) else None

    if not isinstance(id_token, str) or not id_token.strip():
        return jsonify(success=False, message="Token não informado."), 400

    try:
        init_firebase()
    except RuntimeError as exc:
        current_app.logger.error("Firebase não configurado: %s", exc)
        return jsonify(
            success=False,
            code="firebase_configuration_error",
            message=(
                "O servidor precisa das credenciais Firebase do projeto tcc-ecopoint. "
                "Confira FIREBASE_CREDENTIALS no Render ou serviceAccountKey.json localmente."
            ),
        ), 503
    except Exception as exc:
        current_app.logger.error("Falha ao iniciar Firebase: %s", type(exc).__name__)
        return jsonify(
            success=False,
            code="firebase_initialization_error",
            message="Não foi possível iniciar a autenticação no servidor. Confira os logs.",
        ), 503

    try:
        # O SDK continua validando assinatura, emissor, projeto e validade.
        # Tolera apenas uma pequena diferença entre os relógios dos servidores.
        decoded_token = firebase_auth.verify_id_token(id_token, clock_skew_seconds=30)
    except firebase_auth.ExpiredIdTokenError:
        return jsonify(
            success=False,
            code="token_expired",
            message="Sua autenticação expirou. Clique em entrar novamente.",
        ), 401
    except firebase_auth.CertificateFetchError:
        current_app.logger.error("Firebase: falha ao buscar certificados de validação.")
        return jsonify(
            success=False,
            code="certificate_fetch_error",
            message="O servidor não conseguiu consultar o Firebase. Tente novamente em instantes.",
        ), 503
    except firebase_auth.InvalidIdTokenError as exc:
        # Não imprime tokens, e-mails ou credenciais. Registra só a categoria.
        detail = str(exc).lower()
        if "used too early" in detail or "future" in detail:
            code = "server_clock_error"
            message = "O horário do servidor está fora de sincronia. Sincronize o relógio e tente novamente."
        elif '"aud"' in detail or '"iss"' in detail:
            code = "firebase_project_mismatch"
            message = "O login e o servidor precisam usar o mesmo projeto Firebase: tcc-ecopoint."
        else:
            code = "invalid_token"
            message = "A autenticação foi recusada pelo servidor. Entre novamente; se persistir, confira os logs."
        current_app.logger.warning("Falha ao validar token Firebase: %s", code)
        return jsonify(success=False, code=code, message=message), 401
    except Exception as exc:
        current_app.logger.error("Falha ao validar token Firebase: %s", type(exc).__name__)
        return jsonify(
            success=False,
            code="firebase_validation_error",
            message="Não foi possível validar o login no servidor. Confira os logs e tente novamente.",
        ), 503

    uid = decoded_token.get("uid")
    if not uid:
        return jsonify(success=False, message="Token sem identificador de usuário."), 401

    session.clear()
    session.permanent = True
    session["uid"] = uid
    session["email"] = decoded_token.get("email") or ""
    session["nome"] = decoded_token.get("name") or ""

    try:
        usuario = garantir_usuario(
            uid=uid,
            nome=session.get("nome", ""),
            email=session.get("email", ""),
        )
    except Exception as exc:
        session.clear()
        print(f"Falha ao carregar perfil no Firestore: {type(exc).__name__}: {exc}")
        return jsonify(
            success=False,
            message="Login validado, mas não foi possível carregar seu perfil agora.",
        ), 503

    if usuario.get("nome"):
        session["nome"] = usuario["nome"]
    session["tipo"] = usuario.get("tipo", "usuario")

    return jsonify(success=True, tipo=session["tipo"])


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
