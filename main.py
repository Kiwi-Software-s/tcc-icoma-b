import os

from flask import Flask, render_template, request

from app.controllers.auth_controller import auth_bp, login_required
from app.controllers.home_controller import home_bp

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "troque-esta-chave-em-producao")

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)


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
    return render_template("ecopoints/descontos.html", active="descontos")


@app.route("/historico")
@login_required
def historico():
    return render_template("ecopoints/historico.html", active="historico")


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
