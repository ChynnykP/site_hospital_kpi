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
        return f'{self.idDoctor} {self.first_name} {self.last_name} {self.branch} {self.login}'


class Patient(db.Model, UserMixin):
    __table__ = db.Model.metadata.tables['patientdb.patient']

    def get_id(self):
        return (self.idPatient)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'{self.idPatient} {self.first_name} {self.last_name} {self.login}'


class Diseases(db.Model):
    __table__ = db.Model.metadata.tables['patientdb.diseases']

    def __repr__(self):
        return f'{self.idDiseases} {self.name_diseases} {self.status_patient}'


class Medicine(db.Model):
    __table__ = db.Model.metadata.tables['patientdb.medicine']

    def __repr__(self):
        return f'{self.idMedicine} {self.name_medicine}'


class Visiting(db.Model):
    __table__ = db.Model.metadata.tables['patientdb.visiting']

    def __repr__(self):
        return f'{self.idVisiting} {self.date_visiting} {self.Patient_idPatient} {self.Doctor_idDoctor}'


class PatientHasDoctor(db.Model):
    __table__ = db.Model.metadata.tables['patientdb.patient_has_doctor']

    def __repr__(self):
        return f'{self.Patient_idPatient} {self.Doctor_idDoctor} {self.idPatientHasDoctor}'


class PatientHasDiseases(db.Model):
    __table__ = db.Model.metadata.tables['patientdb.patient_has_diseases']

    def __repr__(self):
        return f'{self.Patient_idPatient} {self.Diseases_idDiseases}'


class PatientHasMedicine(db.Model):
    __table__ = db.Model.metadata.tables['patientdb.patient_has_medicine']

    def __repr__(self):
        return f'{self.Patient_idPatient} {self.Medicine_idMedicine}'


class DoctorInsertDiseases(db.Model):
    __table__ = db.Model.metadata.tables['patientdb.doctor_insert_diseases']

    def __repr__(self):
        return f'{self.Doctor_idDoctor} {self.Diseases_idDiseases}'
