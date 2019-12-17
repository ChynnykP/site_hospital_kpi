from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
db = SQLAlchemy(app)
db.Model.metadata.reflect(bind=db.engine, shema='patientdb')
app.config.from_object(Config)
login = LoginManager(app)

from app import routes, models