from flask import Blueprint, jsonify, render_template, request, session

from app.controllers.auth_controller import login_required
from app.repositories.admin_repository import listar_codigos, listar_usuarios, alterar_tipo
from app.repositories.user_repository import (
    atualizar_nome_usuario,
    garantir_usuario,
    obter_tipo_usuario,
    obter_usuario,
)
from app.servicies.beneficio_service import (
    BeneficioInvalidoError,
    definir_favorito,
    listar_beneficios,
    listar_favoritos_usuario,
    montar_historico_usuario,
)
from app.servicies.funcionario_service import criar_codigo
from app.servicies.resgate_service import (
    CodigoInvalidoError,
    CodigoJaUsadoError,
    montar_metricas_dashboard,
    ranking_semanal,
    resgatar_codigo,
)

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

    usuario = garantir_usuario(uid, nome, email)
    if usuario.get("nome"):
        session["nome"] = usuario["nome"]

    metricas = montar_metricas_dashboard(uid)
    ranking = ranking_semanal(uid)
    beneficios_dashboard = listar_beneficios()[:3]

    return render_template(
        "dashboard/dashboard.html",
        nome=session.get("nome") or "Usuário",
        ranking=ranking,
        beneficios_dashboard=beneficios_dashboard,
        **metricas,
    )


@home_bp.route("/mapa-de-pontos")
@login_required
def mapa_de_pontos():
    return render_template("mapa/mapa.html")


@home_bp.route("/perfil")
@login_required
def perfil():
    uid = session["uid"]
    garantir_usuario(uid, session.get("nome", ""), session.get("email", ""))
    usuario = obter_usuario(uid)
    historico = montar_historico_usuario(uid)
    favoritos = listar_favoritos_usuario(uid)

    return render_template(
        "ecopoints/perfil.html",
        active="perfil",
        usuario=usuario,
        favoritos_total=len(favoritos),
        **historico,
    )


@home_bp.route("/api/perfil/nome", methods=["POST"])
@login_required
def api_atualizar_nome():
    dados = request.get_json(silent=True) or {}
    try:
        nome = atualizar_nome_usuario(session["uid"], dados.get("nome", ""))
    except ValueError as exc:
        return jsonify(success=False, message=str(exc)), 400
    except Exception as exc:
        print(f"Erro ao atualizar perfil: {type(exc).__name__}: {exc}")
        return jsonify(success=False, message="Não foi possível atualizar o perfil agora."), 500

    session["nome"] = nome
    return jsonify(success=True, nome=nome)


@home_bp.route("/api/favoritos/<beneficio_id>", methods=["POST"])
@login_required
def api_favorito(beneficio_id):
    dados = request.get_json(silent=True) or {}
    favorito = dados.get("favorito")
    if not isinstance(favorito, bool):
        return jsonify(success=False, message="Estado de favorito inválido."), 400

    try:
        favoritos = definir_favorito(session["uid"], beneficio_id, favorito)
    except BeneficioInvalidoError as exc:
        return jsonify(success=False, message=str(exc)), 404
    except Exception as exc:
        print(f"Erro ao salvar favorito: {type(exc).__name__}: {exc}")
        return jsonify(success=False, message="Não foi possível salvar o favorito agora."), 500

    return jsonify(success=True, favorito=favorito, favoritos=favoritos)


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
        print(f"Erro ao resgatar código: {type(exc).__name__}: {exc}")
        return jsonify(success=False, message="Não foi possível resgatar o código agora."), 500

    return jsonify(success=True, **resultado)



def _tem_acesso(tipos):
    return obter_tipo_usuario(session["uid"]) in tipos

@home_bp.route("/funcionario")
@login_required
def funcionario():
    if not _tem_acesso(["funcionario","admin"]):
        return "Acesso negado", 403
    return render_template("ecopoints/funcionario.html")

@home_bp.route("/admin")
@login_required
def admin():
    if not _tem_acesso(["admin"]):
        return "Acesso negado", 403
    return render_template(
        "ecopoints/admin.html",
        usuarios=listar_usuarios(),
        codigos=listar_codigos()
    )

@home_bp.route("/admin/tipo", methods=["POST"])
@login_required
def admin_tipo():
    if not _tem_acesso(["admin"]):
        return jsonify(success=False, message="Sem permissão"),403
    dados=request.get_json(silent=True) or {}
    try:
        alterar_tipo(dados.get("uid"), dados.get("tipo"))
        return jsonify(success=True)
    except Exception as exc:
        return jsonify(success=False,message=str(exc)),400

@home_bp.route("/funcionario/gerar", methods=["POST"])
@login_required
def funcionario_gerar():
    if not _tem_acesso(["funcionario","admin"]):
        return jsonify(success=False,message="Sem permissão"),403
    dados=request.get_json(silent=True) or {}
    try:
        resultado=criar_codigo(dados.get("material"), dados.get("kg"), session["uid"])
        return jsonify(success=True, **resultado)
    except Exception as exc:
        return jsonify(success=False, message=str(exc)),400
