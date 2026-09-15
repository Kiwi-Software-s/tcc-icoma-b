from flask import Blueprint, render_template, session

from app.controllers.auth_controller import login_required

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
    return render_template("index.html", site="icoma.com.br")


@home_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard/dashboard.html", nome=session.get("nome"))


@home_bp.route("/mapa-de-pontos")
@login_required
def mapa_de_pontos():
    return render_template("mapa/mapa.html")
