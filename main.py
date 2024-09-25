# import eventlet
# eventlet.monkey_patch()
import werkzeug.serving
from flask_cors import CORS
from constants import Constants
from src.connector import app, socketio
from src.utils.database_utils import DatabaseUtils
from src.app import jwt


def run_server():
    cors = CORS(app)
    DatabaseUtils.init_cluster_db(Constants.DATABASE_URL)
    
    # werkzeug.run_simple('0.0.0.0', int(Constants.PORT),
    #                     app, use_debugger=True, use_reloader=True)
    socketio.run(app, host='0.0.0.0', port=int(Constants.PORT), debug=True, use_reloader=True)


if __name__ == '__main__':
    run_server()
