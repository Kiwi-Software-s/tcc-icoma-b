import functools

from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from firebase_admin import auth as firebase_auth

from app.firebase_config import init_firebase
<<<<<<< HEAD
from app.repositories.user_repository import garantir_usuario, obter_tipo_usuario
=======
from app.repositories.user_repository import garantir_usuario
>>>>>>> 00cb19d9a33f9dbe87dcea517577a29742de9f70


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
    data = request.get_json(silent=True) or {}
    id_token = data.get("idToken")

    if not id_token:
        return jsonify(success=False, message="Token não informado."), 400

    try:
        init_firebase()
        decoded_token = firebase_auth.verify_id_token(id_token)
    except RuntimeError as exc:
        print(f"Firebase não configurado: {exc}")
        return jsonify(
            success=False,
            message="O servidor de autenticação não está configurado neste ambiente.",
        ), 503
    except Exception as exc:
        print(f"Falha ao validar token Firebase: {type(exc).__name__}")
        return jsonify(success=False, message="Token inválido ou expirado."), 401

    uid = decoded_token.get("uid")
    if not uid:
        return jsonify(success=False, message="Token sem identificador de usuário."), 401
<<<<<<< HEAD
=======

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

    garantir_usuario(
        uid=session["uid"],
        nome=session.get("nome", ""),
        email=session.get("email", ""),
    )
>>>>>>> 00cb19d9a33f9dbe87dcea517577a29742de9f70

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
