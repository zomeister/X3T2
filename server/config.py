# ./server/config.py - DO NOT EDIT UNLESS YOU HAVE A SPECIFIC REASON!!!!

from flask import Flask
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_cors import CORS
from flask_login import LoginManager
  
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///petapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b"'\xb4\x14f\xfdk\xa8p\xeb\x9d\xf0jmn\x08k"

metadata = MetaData(naming_convention={
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
})
  
db = SQLAlchemy(metadata=metadata)
  
migrate = Migrate(app, db)
db.init_app(app)
  
bcrypt = Bcrypt(app)
  
api = Api(app)
  
CORS(app, resources={r"/api/*": {"origins": "*"}})
  
login_manager = LoginManager()
login_manager.init_app(app)