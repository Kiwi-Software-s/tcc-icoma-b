import os

from flask import Flask, jsonify, render_template, request, session

from app.controllers.auth_controller import auth_bp, login_required
from app.controllers.home_controller import home_bp

from app.repositories.user_repository import garantir_usuario, obter_usuario
from app.servicies.beneficio_service import (
    BeneficioInvalidoError,
    SaldoInsuficienteError,
    listar_beneficios,
    montar_historico_usuario,
    trocar_beneficio,
)
from app.servicies.resgate_service import ranking_semanal

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "troque-esta-chave-em-producao")

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
        print(f"Erro ao trocar benefício: {exc}")
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


@app.after_request
def conectar_links_do_dashboard(response):
    """
    O dashboard atual ainda usa href="#" em alguns itens.
    Este trecho conecta esses links às novas telas sem você precisar
    substituir o dashboard.html existente.
    """
    if request.path != "/dashboard" or not response.content_type.startswith("text/html"):
        return response

    html = response.get_data(as_text=True)

    html = html.replace(
        '<a href="#" class="menu-item">\n'
        '        <span class="menu-icone"><img src="../../static/dashboard/icons/voucher.png" alt=""></span>\n'
        '        Meus descontos',
        '<a href="/meus-descontos" class="menu-item">\n'
        '        <span class="menu-icone"><img src="../../static/dashboard/icons/voucher.png" alt=""></span>\n'
        '        Meus descontos'
    )
    html = html.replace(
        '<a href="#" class="menu-item">\n'
        '        <span class="menu-icone"><img src="../../static/dashboard/icons/replay.png" alt=""></span>\n'
        '        Histórico',
        '<a href="/historico" class="menu-item">\n'
        '        <span class="menu-icone"><img src="../../static/dashboard/icons/replay.png" alt=""></span>\n'
        '        Histórico'
    )
    html = html.replace(
        '<a href="#" class="menu-item">\n'
        '        <span class="menu-icone"><img src="../../static/dashboard/icons/greentech.png" alt=""></span>\n'
        '        Dicas verdes',
        '<a href="/dicas-verdes" class="menu-item">\n'
        '        <span class="menu-icone"><img src="../../static/dashboard/icons/greentech.png" alt=""></span>\n'
        '        Dicas verdes'
    )

    html = html.replace('<a href="#">Meus descontos</a>', '<a href="/meus-descontos">Meus descontos</a>')
    html = html.replace('<a href="#">Dicas verdes</a>', '<a href="/dicas-verdes">Dicas verdes</a>')
    html = html.replace('<a href="#">Resgatar Códigos</a>', '<a href="/resgatar-codigos">Resgatar Códigos</a>')

    response.set_data(html)
    return response


def main():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=True)


if __name__ == "__main__":
    main()
