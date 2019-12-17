from app import db
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


db.Model.metadata.reflect(bind=db.engine, schema='patientdb')

@login.user_loader
def load_user(id_patient):
    return Patient.query.get(int(id_patient))


class Doctor(db.Model, UserMixin):
    __table__ = db.Model.metadata.tables['patientdb.doctor']

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Doctor {self.last_name}>'


class Patient(db.Model, UserMixin):
    __table__ = db.Model.metadata.tables['patientdb.patient']

    def get_id(self):
        return (self.idPatient)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Patient {self.last_name}>'
