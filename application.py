# from flask import Flask
# # from flask_login import LoginManager
# # from flask_sqlalchemy import SQLAlchemy
# # from config import Config
# from flask import render_template, flash, redirect, url_for
# # from forms import LoginForm, RegistrationForm
# # from flask_login import current_user, login_user, logout_user
# # from .models import Patient
#
# app = Flask(__name__)
#
#
# @app.route('/')
# @app.route('/index')
# def index():
#     return render_template('index.html')
#
#
# # @app.route('/login.html', methods=['GET', 'POST'])
# # def login():
# #     if current_user.is_authenticated:
# #         return redirect(url_for('index'))
# #     form = LoginForm()
# #     if form.validate_on_submit():
# #         patient = Patient.query.filter_by(login=form.email.data).first()
# #         if patient is None or not patient.check_password(form.password.data):
# #             flash('Invalid  email or password')
# #             return redirect(url_for('login'))
# #         login_user(patient, remember=form.remember_me.data)
# #         return redirect(url_for('index'))
# #     return render_template('login.html', form=form)
# #
# #
# # @app.route('/logout')
# # def logout():
# #     logout_user()
# #     return redirect(url_for('index'))
# #
# #
# # @app.route('/register', methods=['GET', 'POST'])
# # def register():
# #     if current_user.is_authenticated:
# #         return redirect(url_for('index'))
# #     form = RegistrationForm()
# #     if form.validate_on_submit():
# #         patient = Patient(first_name=form.firstname.data, last_name=form.lastname.data, login=form.email.data)
# #         patient.set_password(form.password.data)
# #         db.session.add(patient)
# #         db.session.commit()
# #         flash('Congratulations, you are now a registered user!')
# #         return redirect(url_for('login'))
# #     return render_template('register.html', form=form)
# #
# # @app.route('/cabynet')
# # def cabynet():
# #     return render_template('cabynet.html')
from app import app

if __name__ == "__main__":
    app.run(debug=True)