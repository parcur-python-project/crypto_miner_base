import os
import sentry_sdk
from flask_mysqldb import MySQL
from flask import Flask, request
from dotenv import load_dotenv
from flask_restful import Api
from sentry_sdk.integrations.flask import FlaskIntegration
from flask_socketio import SocketIO, send, join_room
# import Environment variables
load_dotenv()

# ===============================================================================
#  Flask App Configuration
# ===============================================================================
app = Flask(__name__)  # pylint: disable=invalid-name

base_api_url = "/api"
# CORS(app)
app.config['DEBUG'] = True


# ===============================================================================
# Environment-specific configurations can be done here
# ===============================================================================
if os.environ.get('ENV') == 'development':
    print("Starting application in Development mode...")
    # any config ...
elif os.environ.get('ENV') == 'production':
    print("Starting application in Production mode...")

    # any config ...

if os.environ.get("MYSQL_HOST") != "127.0.0.1" or os.getenv("ENV") != "development":
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[FlaskIntegration()],
        traces_sample_rate=os.getenv('SENTRY_TRACES_SAMPLE')
    )


# ===============================================================================
# MySQL settings
# ===============================================================================
app.sql = MySQL(app)


# ===============================================================================
# before_request(): function which runs before every request is routed to blueprint
# ===============================================================================


@ app.before_request
def before_request():
    if request.path.startswith(base_api_url):
        return 

# ====================================================================================
# after_request(): function which runs after every request is returned from blueprint
# ====================================================================================

@ app.after_request
def after_request(response):
    if app.debug:

        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Content-Type', 'application/json')

        response.headers.add("Access-Control-Allow-Headers",
                             'Content-Type, Access-Control-Allow-Headers X-Forwarded-For, Access-Control-Allow-Origin')

        response.headers.add('Access-Control-Expose-Headers',
                             'Content-Type, Content-Length, Access-Control-Allow-Origin,')

        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PUT, DELETE, OPTIONS, PATCH')

        app.logger.debug('RESPONSE Headers: %s', response.headers)
        app.logger.debug('RESPONSE Body: %s', response.data)
        app.logger.debug('RESPONSE Status: %s %s',
                         response.status_code, response.status)

        return response


# ===============================================================================
# Flask register app and start
# ===============================================================================
api = Api(app, catch_all_404s=True)  # pylint: disable=invalid-name



# Sockets
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('crypto_data_updated')
def crypto_data_retrieved(data):
    # Save in db
    # Send to frontend
    # Update Again
    pass



if __name__ == '__main__':
    socketio.run(app, port=8000, host='0.0.0.0', debug=app.debug)
    # app.run( debug=app.debug, port=8000, host='0.0.0.0')
