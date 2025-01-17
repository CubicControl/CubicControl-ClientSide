import datetime
import secrets

from flask import Flask
from flask_cors import CORS

from routes.routes import bp

app = Flask(__name__)
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)
CORS(app, resources={r"/*": {"origins": ["https://serverwebsite-z5my.onrender.com/"]}})

app.register_blueprint(bp)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
