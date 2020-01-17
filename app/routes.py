from flask import render_template, flash, redirect, url_for, jsonify, request
from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, VisitingForm, IndexForm
from flask_login import current_user, login_user, logout_user
from datetime import datetime
from app.models import Patient, Doctor, Diseases, Medicine, PatientHasDoctor, PatientHasDiseases, PatientHasMedicine, \
    DoctorInsertDiseases, Visiting, City


class TmpIndex:
    def __init__(self, region, service, doctor, date, time):
        self.region = region
        self.service = service
        self.doctor = doctor
        self.date = date
        self.time = time

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = VisitingForm()
    form.region.choices = [(city.name, city.name) for city in City.query.distinct().all()]
    form.branch.choices = [(branch.branch, branch.branch) for branch in Doctor.query.distinct().all()]
    form.doctor.choices = [(doctor.idDoctor, f'{doctor.first_name} {doctor.last_name}') for doctor in
                           Doctor.query.filter_by(branch="therapist").all()]
    return render_template('index.html', form=form)

@app.route('/forward/', methods=["POST"])
def forward():
    # breakpoint()
    region = request.form.get('region')
    branch = request.form.get('branch')
    doctor = request.form.get('doctor')
    date = request.form.get('date')
    time = request.form.get('time')
    name_doctor = doctor.split()
    city = City.query.filter_by(name=region).all()
    visiting = Visiting(date_visiting = date + ' ' + time,
                        Patient_idPatient=current_user.idPatient,
                        Doctor_idDoctor=doctor, City_idCity=city[0].idCity)
    doctor = PatientHasDoctor(Patient_idPatient=current_user.idPatient, Doctor_idDoctor=doctor)
    db.session.add(visiting)
    db.session.add(doctor)
    db.session.commit()
    return redirect(url_for('visiting'))

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        patient = Patient.query.filter_by(login=form.email.data).first()
        if patient is None or not patient.check_password(form.password.data):
            flash('Invalid  email or password')
            return redirect(url_for('login'))
        login_user(patient, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        patient = Patient(first_name=form.firstname.data, last_name=form.lastname.data, login=form.email.data)
        patient.set_password(form.password.data)
        db.session.add(patient)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/cabynet')
def cabynet():
    if current_user.is_anonymous:
        return redirect(url_for('index'))
    return render_template('cabynet.html')


@app.route('/account')
def account():
    if current_user.is_anonymous:
        return redirect(url_for('index'))
    return render_template('account.html')


@app.route('/doctors')
def doctors():
    if current_user.is_anonymous:
        return redirect(url_for('index'))
    doctor = Doctor.query.join(PatientHasDoctor, PatientHasDoctor.Doctor_idDoctor == Doctor.idDoctor).join(Patient,
                                                                                                           current_user.idPatient == PatientHasDoctor.Patient_idPatient)
    return render_template('doctors.html', doctor=doctor)


@app.route('/visiting', methods=['GET', 'POST'])
def visiting():
    if current_user.is_anonymous:
        return redirect(url_for('index'))
    form = VisitingForm()
    form.region.choices = [(city.name, city.name) for city in City.query.distinct().all()]
    form.branch.choices = [(branch.branch, branch.branch) for branch in Doctor.query.distinct().all()]
    form.doctor.choices = [(doctor.idDoctor, f'{doctor.first_name} {doctor.last_name}') for doctor in
                           Doctor.query.filter_by(branch="therapist").all()]
    v = Visiting.query.join(Doctor, Visiting.Doctor_idDoctor == Doctor.idDoctor).join(Patient, Visiting.Patient_idPatient == current_user.idPatient).add_columns( Visiting.date_visiting, Doctor.first_name, Doctor.last_name, Doctor.branch)
    # breakpoint()
    if request.method == 'POST':
        # breakpoint()
        visiting = Visiting(date_visiting=form.date.data.strftime('%Y-%m-%d %H:%M:%S'),
                            Patient_idPatient=current_user.idPatient,
                            Doctor_idDoctor=form.doctor.data)
        doctor = PatientHasDoctor(Patient_idPatient=current_user.idPatient, Doctor_idDoctor=form.doctor.data)
        db.session.add(visiting)
        db.session.add(doctor)
        db.session.commit()
        return redirect(url_for('account'))
    return render_template('visiting.html', form=form, visiting=v)


@app.route('/index/<branch>')
def select_doctor_index(branch):
    doctor = Doctor.query.filter_by(branch=branch).all()

    list_doctor = []

    for d in doctor:
        doctorObj = {}
        doctorObj['idDoctor'] = d.idDoctor
        doctorObj['name'] = d.first_name + ' ' + d.last_name
        list_doctor.append(doctorObj)

    return jsonify({'doctors': list_doctor})
@app.route('/visiting/<branch>')
def select_doctor(branch):
    if current_user.is_anonymous:
        return redirect(url_for('index'))
    doctor = Doctor.query.filter_by(branch=branch).all()

    list_doctor = []

    for d in doctor:
        doctorObj = {}
        doctorObj['idDoctor'] = d.idDoctor
        doctorObj['name'] = d.first_name + d.last_name
        list_doctor.append(doctorObj)

    return jsonify({'doctors': list_doctor})


@app.route('/carta')
def carta():
    if current_user.is_anonymous:
        return redirect(url_for('index'))
    carta = Diseases.query \
        .join(DoctorInsertDiseases, DoctorInsertDiseases.Diseases_idDiseases == Diseases.idDiseases) \
        .join(Doctor, DoctorInsertDiseases.Doctor_idDoctor == Doctor.idDoctor) \
        .outerjoin(PatientHasMedicine, PatientHasMedicine.Diseases_idDiseases == Diseases.idDiseases) \
        .outerjoin(Medicine, PatientHasMedicine.Medicine_idMedicine == Medicine.idMedicine) \
        .join(PatientHasDiseases, PatientHasDiseases.Diseases_idDiseases == Diseases.idDiseases) \
        .join(Patient, PatientHasDiseases.Patient_idPatient == current_user.idPatient) \
        .add_columns(Diseases.name_diseases, Doctor.first_name, Doctor.last_name, Medicine.name_medicine)
    return render_template('carta.html', carta=carta)
