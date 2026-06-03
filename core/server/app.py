from flask import Flask

from core.server.route.default_bp import DEFAULT_BP


def run_app():
    new_app = Flask(__name__)
    new_app.register_blueprint(DEFAULT_BP)
    return new_app

app = run_app()