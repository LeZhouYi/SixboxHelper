from flask import Flask

from core.env import PORT
from core.server.route.default_bp import DEFAULT_BP


def run_app():
    app = Flask(__name__)
    app.register_blueprint(DEFAULT_BP)
    app.run(debug=False, host="0.0.0.0", port=PORT)
