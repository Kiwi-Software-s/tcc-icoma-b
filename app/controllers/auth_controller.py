import functools

from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from firebase_admin import auth as firebase_auth

from app.firebase_config import init_firebase

init_firebase()

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
    """
    Recebe o idToken gerado pelo Firebase no navegador (após login ou
    cadastro com e-mail/senha ou Google), valida no servidor com o
    Firebase Admin SDK e cria a sessão do Flask.
    """
    data = request.get_json(silent=True) or {}
    id_token = data.get("idToken")

    if not id_token:
        return jsonify(success=False, message="Token não informado."), 400

    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
    except Exception:
        return jsonify(success=False, message="Token inválido ou expirado."), 401

    session["uid"] = decoded_token.get("uid")
    session["email"] = decoded_token.get("email")
    session["nome"] = decoded_token.get("name", "")

    return jsonify(success=True)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
