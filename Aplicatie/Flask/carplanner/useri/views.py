from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from carplanner import db, app
from werkzeug.security import generate_password_hash,check_password_hash
from carplanner.models import User, Masina, Marca, Scadent
from carplanner.useri.forms import RegistrationForm, LoginForm, UpdateUserForm, ForgotForm
from carplanner.useri.picture_handler import add_profile_pic


useri = Blueprint('useri', __name__)


@useri.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
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
  if form.validate_on_submit():
    # Grab the user from our User Models table
    user = User.query.filter_by(email = form.email.data).first()

    # Check that the user was supplied and the password is right
    # The verify_password method comes from the User object
    # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not
    if user is not None and user.check_password(form.parola.data):
      #Log in the user
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
  if form.validate_on_submit():

    # Grab the user from our User Models table
    user = User.query.filter_by(email=form.email.data).first()

    if user is not None:
      flash('Un mail cu link de activare a fost trimis la mailul introdus')
      # Trebuie sa trimitem si linkul!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    else:
      flash('Nu avem in baza de date acest mail')
  return render_template('uitatparola.html', form=form)


@useri.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for('core.index'))


@useri.route("/<email>/updateuser", methods=['GET', 'POST'])
@login_required
def updateuser(email):
  if email != current_user.email:
    # Forbidden, No Access
    abort(403)
  form = UpdateUserForm()

  if form.validate_on_submit():
    if form.picture.data:
      email = current_user.email
      pic = add_profile_pic(form.picture.data, email)
      current_user.imagineProfil = pic

    current_user.email = form.email.data
    current_user.numeUser = form.numeUser.data
    current_user.prenumeUser = form.prenumeUser.data
    current_user.numeCompanie = form.numeCompanie.data
    if form.parola.data:
      current_user.parola=generate_password_hash(form.parola.data)

    db.session.commit()
    flash('Datele contului au fost actualizate cu succes.')
    return redirect(url_for('useri.userhome', email=current_user.email))

  elif request.method == 'GET':
    form.email.data = current_user.email
    form.numeUser.data = current_user.numeUser
    form.prenumeUser.data = current_user.prenumeUser
    form.numeCompanie.data = current_user.numeCompanie


  imagineProfil = url_for('static', filename='profile_pics/' + current_user.imagineProfil)
  return render_template('updateuser.html', imagineProfil=imagineProfil, form=form)


@useri.route("/<email>/removeuser", methods=['GET', 'POST'])
@login_required
def removeuser(email):
  if email != current_user.email:
    # Forbidden, No Access
    abort(403)
    return render_template('removeuser.html', email=email)

@useri.route("/<email>/removeuseryes", methods=['GET', 'POST'])
@login_required
def removeuseryes(email):
  if email != current_user.email:
    # Forbidden, No Access
    abort(403)
  user = db.session.query(User).filter(User.email == email).first()
  masini = db.session.query(Masina).filter(Masina.IDUser == user.IDUser).all()
  for masina in masini:
    scadente = db.session.query(Scadent).filter(Scadent.IDMasina == masina.IDMasina).delete()
    masina = db.session.query(Masina).filter(Masina.IDMasina == masina.IDMasina).delete()

  logout_user()

  db.session.delete(user)

  db.session.commit()


  flash("Ne pare rau ca pleci! Contul tau a fost sters cu scucces")

  return render_template('index.html')



@useri.route("/<email>")
@login_required
def userhome(email):

  if email != current_user.email:
    # Forbidden, No Access
    abort(403)

  user = User.query.filter_by(email=email).first_or_404()
  masini = []
  i = 0
  for masina, marca in db.session.query(Masina, Marca).filter(Masina.IDAuto == Marca.IDAuto, Masina.proprietar == user).all():
    scadentMaximDate = Scadent.query.filter_by(IDMasina = masina.IDMasina).order_by(Scadent.dataExp.asc()).first()
    scadentMaximKm = db.session.query(Scadent).filter(Scadent.IDMasina == masina.IDMasina, Scadent.areKM == 1).order_by(Scadent.kmExp.asc()).first()

    if scadentMaximDate is None:
      scadentMaximDateAfis = "NA"
    else:
      scadentMaximDateAfis = scadentMaximDate.dataExp
    if scadentMaximKm is None:
      scadentMaximKmAfis = "NA"
    else:
      scadentMaximKmAfis = scadentMaximKm.kmExp

    i = i + 1
    masini.append({"id" : i, "IDMasina" : masina.IDMasina,"marcaMasina" : marca.marcaMasina, "modelMasina" : marca.modelMasina, "numarInmatriculare" : masina.numarInmatriculare, "kilometraj" : masina.kilometraj, "scadentData" : scadentMaximDateAfis, "scadentKm" : scadentMaximKmAfis})

  if current_user.prenumeUser is None or current_user.prenumeUser == "" or current_user.prenumeUser == " ":
    nume = current_user.email.split("@")[0]
  else:
    nume = current_user.prenumeUser

  return render_template('userhome.html', masini=masini, user=user, nume=nume)
