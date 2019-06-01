from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from carplanner import db, app
from werkzeug.security import generate_password_hash,check_password_hash
from carplanner.models import User, Masina
from carplanner.useri.forms import RegistrationForm, LoginForm, UpdateUserForm, ForgotForm
from carplanner.useri.picture_handler import add_profile_pic



useri = Blueprint('useri', __name__)


@useri.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  app.logger.info("Am intrat in register")
  if form.validate_on_submit():
    app.logger.info("Am intrat in register -> validate_on_submit")
    user = User(email=form.email.data,
                numeUser=form.numeUser.data,
                prenumeUser=form.prenumeUser.data,
                numeCompanie=form.numeCompanie.data,
                parola=form.parola.data)

    db.session.add(user)
    db.session.commit()
    flash('Multumim pentru inregistrare! Te poti loga acum.')
    return redirect(url_for('useri.login'))
  return render_template('register.html', form=form)

@useri.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  app.logger.info("Am intrat in login")
  if form.validate_on_submit():
    app.logger.info("Am intrat in login -> validate_on_submit")
    # Grab the user from our User Models table
    user = User.query.filter_by(email = form.email.data).first()

    # Check that the user was supplied and the password is right
    # The verify_password method comes from the User object
    # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not
    if user is not None and user.check_password(form.parola.data):
      #Log in the user
      app.logger.info("Am intrat in login -> check_password")
      login_user(user)

      # If a user was trying to visit a page that requires a login
      # flask saves that URL as 'next'.
      next = request.args.get('next')

      # So let's now check if that next exists, otherwise we'll go to
      # the welcome page.
      if next == None or not next[0]=='/':
        next = url_for('useri.userhome', email=user.email)

      return redirect(next)
    else:
      flash('Email sau parola gresita!')

  return render_template('login.html', form=form)


@useri.route('/uitatparola', methods=['GET', 'POST'])
def uitatparola():
  form = ForgotForm()
  app.logger.info("Am intrat in uitatparola")
  if form.validate_on_submit():
    app.logger.info("Am intrat in uitatparola -> validate_on_submit")

    # Grab the user from our User Models table
    user = User.query.filter_by(email=form.email.data).first()

    if user is not None:
      flash('Un mail cu link de activare a fost trimis la mailul introdus')
      # Trebuie sa trimitem si linkul!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    else:
      flash('Nu avem in baza de date acest mail')
  return render_template('uitatparola.html', form=form)



@useri.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('core.index'))



@useri.route("/updateuser", methods=['GET', 'POST'])
@login_required
def updateuser():
  form = UpdateUserForm()
  app.logger.info("Am intrat in updateuser")

  if form.validate_on_submit():
    app.logger.info("Am intrat in updateuser -> validate_on_submit")
    if form.picture.data:
      email = current_user.email
      pic = add_profile_pic(form.picture.data, email)
      current_user.imagineProfil = pic
    app.logger.info("Am trecut de functie")

    current_user.email = form.email.data
    current_user.numeUser = form.numeUser.data
    current_user.prenumeUser = form.prenumeUser.data
    current_user.numeCompanie = form.numeCompanie.data
    current_user.parola=generate_password_hash(form.parola.data)

    db.session.commit()
    flash('Datele contului au fost actualizate cu succes.')
    return redirect(url_for('useri.updateuser'))

  elif request.method == 'GET':
    form.email.data = current_user.email
    form.numeUser.data = current_user.numeUser
    form.prenumeUser.data = current_user.prenumeUser
    form.numeCompanie.data = current_user.numeCompanie

  if current_user.prenumeUser != None:
    nume = current_user.prenumeUser
  else:
    nume = current_user.email.split("@")[0]
  imagineProfil = url_for('static', filename='profile_pics/' + current_user.imagineProfil)
  return render_template('updateuser.html', imagineProfil=imagineProfil, form=form, nume=nume)


@useri.route("/<email>")
def userhome(email):
  page = request.args.get('page', 1, type=int)
  user = User.query.filter_by(email=email).first_or_404()
  masini = []#Masina.query.filter_by(proprietar=user).paginate(page=page, per_page=5)
  if user.prenumeUser != None:
    nume = user.prenumeUser
  else:
    nume = user.email.split("@")[0]
  return render_template('userhome.html', masini=masini, user=user, nume=nume)
