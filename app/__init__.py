from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
#from flask_cors import CORS

def create_app(config=None):
    app = Flask(__name__,  static_folder = "templates/static", template_folder='templates')
    app.config.from_object(Config)
    app.config['TESTING'] = True
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    return app

app = create_app()
#CORS(app)
#ORM init
db = SQLAlchemy(app)
#serialization tool
ma = Marshmallow(app)
#Migration init
migrate = Migrate(app, db)
#Flask-Login init
login = LoginManager()
login.init_app(app)
# SocketIO init

from app import routes, app_methods

if __name__ == '__main__':
    app.run()
