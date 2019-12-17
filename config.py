import os

IP_DATABASE_AZURE = "patientdb.mysql.database.azure.com"
IP_DATABASE_IASA = "zanner.org.ua"


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KET') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://petro@patientdb:Ghjuhfvscn_[frth1@{IP_DATABASE_AZURE}:3306/patientdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False