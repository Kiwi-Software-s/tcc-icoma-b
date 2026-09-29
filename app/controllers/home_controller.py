from flask import Blueprint, jsonify, render_template, request, session

from app.controllers.auth_controller import login_required
from app.repositories.user_repository import garantir_usuario
from app.servicies.resgate_service import (
    CodigoInvalidoError,
    CodigoJaUsadoError,
    montar_metricas_dashboard,
    ranking_semanal,
    resgatar_codigo,
)
from app.servicies.beneficio_service import listar_beneficios

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
    return render_template("index.html", site="icoma.com.br")


@home_bp.route("/dashboard")
@login_required
def dashboard():
    uid = session.get("uid")
    nome = session.get("nome", "")
    email = session.get("email", "")

    garantir_usuario(uid, nome, email)
    metricas = montar_metricas_dashboard(uid)
    ranking = ranking_semanal(uid)

    beneficios_dashboard = listar_beneficios()[:3]

    return render_template(
        "dashboard/dashboard.html",
        nome=nome,
        ranking=ranking,
        beneficios_dashboard=beneficios_dashboard,
        **metricas,
    )


@home_bp.route("/mapa-de-pontos")
@login_required
def mapa_de_pontos():
    return render_template("mapa/mapa.html")


@home_bp.route("/api/resgatar-codigo", methods=["POST"])
@login_required
def api_resgatar_codigo():
    dados = request.get_json(silent=True) or {}
    codigo = dados.get("codigo", "")

    try:
        resultado = resgatar_codigo(
            uid=session["uid"],
            codigo=codigo,
            nome_usuario=session.get("nome", ""),
            email_usuario=session.get("email", ""),
        )
    except CodigoInvalidoError as exc:
        return jsonify(success=False, message=str(exc)), 404
    except CodigoJaUsadoError as exc:
        return jsonify(success=False, message=str(exc)), 409
    except Exception as exc:
        print(f"Erro ao resgatar código: {exc}")
        return jsonify(success=False, message="Não foi possível resgatar o código agora."), 500

    return jsonify(success=True, **resultado)
