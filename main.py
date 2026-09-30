import os
from datetime import datetime, timedelta

from flask import Flask, jsonify, render_template, request, session

from app.controllers.auth_controller import auth_bp, login_required
from app.controllers.home_controller import home_bp

from app.repositories.user_repository import garantir_usuario, obter_usuario
from app.servicies.beneficio_service import (
    BeneficioInvalidoError,
    SaldoInsuficienteError,
    listar_beneficios,
<<<<<<< HEAD
    listar_favoritos_usuario,
=======
>>>>>>> 40045d14bc5afcf18652c9804bdce5877a5f3ee6
    montar_historico_usuario,
    trocar_beneficio,
)
from app.servicies.resgate_service import ranking_semanal

<<<<<<< HEAD

IS_PRODUCTION = (
    os.environ.get("RENDER", "").lower() == "true"
    or os.environ.get("FLASK_ENV", "").lower() == "production"
)

=======
>>>>>>> 40045d14bc5afcf18652c9804bdce5877a5f3ee6
app = Flask(__name__)

secret_key = os.environ.get("FLASK_SECRET_KEY")
if not secret_key:
    if IS_PRODUCTION:
        raise RuntimeError("Defina FLASK_SECRET_KEY antes de iniciar em produção.")
    secret_key = "ecopoints-dev-only-change-me"

app.secret_key = secret_key
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=IS_PRODUCTION,
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),
    MAX_CONTENT_LENGTH=2 * 1024 * 1024,
)

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)


@app.template_filter("fmt_int")
def fmt_int(value):
    try:
        return f"{int(value):,}".replace(",", ".")
    except (TypeError, ValueError):
        return "0"


@app.template_filter("fmt_num")
def fmt_num(value):
    try:
        numero = float(value)
    except (TypeError, ValueError):
        numero = 0.0

    if numero.is_integer():
        return f"{int(numero):,}".replace(",", ".")

    texto = f"{numero:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".").rstrip("0").rstrip(",")


<<<<<<< HEAD
@app.template_filter("fmt_date")
def fmt_date(value):
    if not value:
        return "—"
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y")
    return str(value)


@app.route("/health")
def health():
    return jsonify(status="ok", app="ecopoints")


=======
>>>>>>> 40045d14bc5afcf18652c9804bdce5877a5f3ee6
@app.route("/dicas-verdes")
@login_required
def dicas_verdes():
    return render_template("ecopoints/dicas_verdes.html")


@app.route("/resgatar-codigos")
@login_required
def resgatar_codigos():
    return render_template("ecopoints/resgatar_codigos.html", active="resgate")


@app.route("/meus-descontos")
@login_required
def meus_descontos():
    uid = session["uid"]
    garantir_usuario(uid, session.get("nome", ""), session.get("email", ""))
    usuario = obter_usuario(uid)
    return render_template(
        "ecopoints/descontos.html",
        active="descontos",
        beneficios=listar_beneficios(),
<<<<<<< HEAD
        favoritos=listar_favoritos_usuario(uid),
=======
>>>>>>> 40045d14bc5afcf18652c9804bdce5877a5f3ee6
        pontos_total=int(usuario.get("pontos_total", 0) or 0),
        ranking=ranking_semanal(uid),
    )


@app.route("/api/trocar-beneficio", methods=["POST"])
@login_required
def api_trocar_beneficio():
    dados = request.get_json(silent=True) or {}
    beneficio_id = dados.get("beneficio_id", "")

    try:
        resultado = trocar_beneficio(
            uid=session["uid"],
            beneficio_id=beneficio_id,
            nome_usuario=session.get("nome", ""),
            email_usuario=session.get("email", ""),
        )
    except BeneficioInvalidoError as exc:
        return jsonify(success=False, message=str(exc)), 404
    except SaldoInsuficienteError as exc:
        return jsonify(success=False, message=str(exc)), 409
    except Exception as exc:
<<<<<<< HEAD
        print(f"Erro ao trocar benefício: {type(exc).__name__}: {exc}")
=======
        print(f"Erro ao trocar benefício: {exc}")
>>>>>>> 40045d14bc5afcf18652c9804bdce5877a5f3ee6
        return jsonify(success=False, message="Não foi possível concluir a troca agora."), 500

    return jsonify(success=True, **resultado)


@app.route("/historico")
@login_required
def historico():
    dados = montar_historico_usuario(session["uid"])
    return render_template(
        "ecopoints/historico.html",
        active="historico",
        **dados,
    )
<<<<<<< HEAD


@app.errorhandler(404)
def pagina_nao_encontrada(error):
    if request.path.startswith("/api/"):
        return jsonify(success=False, message="Recurso não encontrado."), 404
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def erro_interno(error):
    if request.path.startswith("/api/"):
        return jsonify(success=False, message="Ocorreu um erro interno. Tente novamente."), 500
    return render_template("errors/500.html"), 500
=======
>>>>>>> 40045d14bc5afcf18652c9804bdce5877a5f3ee6


@app.after_request
def security_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    return response


def main():
    debug_env = os.environ.get("FLASK_DEBUG")
    debug = (debug_env == "1") if debug_env is not None else (not IS_PRODUCTION)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=debug)


if __name__ == "__main__":
    main()
