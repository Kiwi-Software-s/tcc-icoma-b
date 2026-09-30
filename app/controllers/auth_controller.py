import functools

from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from firebase_admin import auth as firebase_auth

from app.firebase_config import init_firebase
from app.repositories.user_repository import garantir_usuario


auth_bp = Blueprint("auth", __name__)


def login_required(view):
    """Decorator que protege rotas exigindo uma sessão autenticada."""
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("uid"):
            return redirect(url_for("auth.login"))
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

    return jsonify(success=True)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
