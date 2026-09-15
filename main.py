import os

from flask import Flask

from app.controllers.auth_controller import auth_bp
from app.controllers.home_controller import home_bp

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "troque-esta-chave-em-producao")

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)


def main():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=True)


if __name__ == "__main__":
    main()
