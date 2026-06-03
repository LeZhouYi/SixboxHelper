from core.env import PORT
from core.log.logger import init_log
from core.server.app import app

if __name__ == "__main__":
    init_log()
    app.run(debug=False, host="0.0.0.0", port=PORT)