from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import current_user, login_required

from carplanner import db, app
from carplanner.models import Scadent, Masina, RevizieDefault
from carplanner.scadente.forms import DefaultScadentForm, AddScadentForm, EditScadentForm
import datetime

scadente = Blueprint('scadente',__name__)


@scadente.route('/<email>/<numarInmatriculare>/defaultscadent',methods=['GET','POST'])
@login_required
def defaultScadent(email, numarInmatriculare):
  if email != current_user.email:
    # Forbidden, No Access
    abort(403)
  now = datetime.datetime.now()
  form = DefaultScadentForm()

  if form.validate_on_submit():

    scadente = []
    if form.default1.data is True:
      masina = Masina.query.filter_by(numarInmatriculare = numarInmatriculare, IDUser = current_user.IDUser).first()
      revizieDefault = RevizieDefault.query.filter_by(IDAuto = masina.IDAuto, numeSchimb="Ulei + filtre").first()
      scadenta = Scadent(revizieDefault.IDRevizie, revizieDefault.numeSchimb, masina.IDMasina, now + datetime.timedelta(revizieDefault.viataZile), True, masina.kilometraj + revizieDefault.viataKm, revizieDefault.viataZile, revizieDefault.viataKm)
      scadente.append(scadenta)

    if form.default2.data is True:
      masina = Masina.query.filter_by(numarInmatriculare = numarInmatriculare, IDUser = current_user.IDUser).first()
      revizieDefault = RevizieDefault.query.filter_by(IDAuto = masina.IDAuto, numeSchimb="Distributie").first()
      scadenta = Scadent(revizieDefault.IDRevizie, revizieDefault.numeSchimb, masina.IDMasina, now + datetime.timedelta(revizieDefault.viataZile), True, masina.kilometraj + revizieDefault.viataKm, revizieDefault.viataZile, revizieDefault.viataKm)
      scadente.append(scadenta)

    if form.default3.data is True:
      masina = Masina.query.filter_by(numarInmatriculare = numarInmatriculare, IDUser = current_user.IDUser).first()
      revizieDefault = RevizieDefault.query.filter_by(IDAuto = masina.IDAuto, numeSchimb="Elemente franare").first()
      scadenta = Scadent(revizieDefault.IDRevizie, revizieDefault.numeSchimb, masina.IDMasina, now + datetime.timedelta(revizieDefault.viataZile), True, masina.kilometraj + revizieDefault.viataKm, revizieDefault.viataZile, revizieDefault.viataKm)
      scadente.append(scadenta)

    if form.default4.data is True:
      masina = Masina.query.filter_by(numarInmatriculare = numarInmatriculare, IDUser = current_user.IDUser).first()
      revizieDefault = RevizieDefault.query.filter_by(IDAuto = masina.IDAuto, numeSchimb="Baterie").first()
      scadenta = Scadent(revizieDefault.IDRevizie, revizieDefault.numeSchimb, masina.IDMasina, now + datetime.timedelta(revizieDefault.viataZile), True, masina.kilometraj + revizieDefault.viataKm, revizieDefault.viataZile, revizieDefault.viataKm)
      scadente.append(scadenta)


    db.session.add_all(scadente)
    db.session.commit()
    flash("Reviziile default selectate au fost adaugate cu succes masinii tale")

    return redirect(url_for('useri.userhome', email=current_user.email))



  return render_template('defaultscadent.html', form=form)


@scadente.route('/<email>/<IDMasina>/add',methods=['GET','POST'])
@login_required
def addScadent(email, IDMasina):
  if email != current_user.email:
    # Forbidden, No Access
    abort(403)

  form = AddScadentForm()

  if form.validate_on_submit():
    now = datetime.datetime.now()
    masina = Masina.query.filter_by(IDMasina = IDMasina).first()
    if form.viataKm.data == 0 or form.viataKm.data is None or form.viataKm.data == "" :
      scadent = Scadent(1, form.numeScadent.data, IDMasina, now + datetime.timedelta(int(form.viataZile.data)), False, 0, int(form.viataZile.data), 0)
    else:
      scadent = Scadent(1, form.numeScadent.data, IDMasina, now + datetime.timedelta(int(form.viataZile.data)), True, masina.kilometraj + int(form.viataKm.data), int(form.viataZile.data), int(form.viataKm.data))

    db.session.add(scadent)
    db.session.commit()
    flash('Scadentul a fost adaugat cu succces!')
    return redirect(url_for('masini.detailsVehicle', email=email, IDMasina=IDMasina))


  return render_template('addscadent.html', form=form, IDMasina=IDMasina)






@scadente.route('/<email>/<IDMasina>/<IDScadent>/edit',methods=['GET','POST'])
@login_required
def editScadent(email, IDMasina, IDScadent):
  if email != current_user.email:
    # Forbidden, No Access
    abort(403)
  form = EditScadentForm()
  scadent = db.session.query(Scadent).filter(Scadent.IDScadent == IDScadent).first()
  now = datetime.datetime.now()
  masina = Masina.query.filter_by(IDMasina = IDMasina).first()

  if form.validate_on_submit():


    scadent.numeScadent = form.numeScadent.data
    scadent.dataExp = now + datetime.timedelta(int(form.viataZile.data))

    if form.viataKm.data == 0 or form.viataKm.data is None or form.viataKm.data == "" :
      scadent.areKM = False
      scadent.kmExp = 0
    else:
      scadent.areKM = True
      scadent.kmExp = masina.kilometraj + int(form.viataKm.data)


    db.session.commit()
    flash('Datele scadentului au fost actualizate cu succes.')
    return redirect(url_for('masini.detailsVehicle', email=email, IDMasina=IDMasina))

  elif request.method == 'GET':
    form.numeScadent.data = scadent.numeScadent
    form.viataZile.data = scadent.viataZile
    form.viataKm.data = scadent.viataKm


  return render_template('editscadent.html', form=form, IDMasina=IDMasina)


@scadente.route('/<email>/<IDMasina>/<IDScadent>/remove',methods=['GET','POST'])
@login_required
def removeScadent(email, IDMasina, IDScadent):
  if email != current_user.email:
    # Forbidden, No Access
    abort(403)
  scadent = db.session.query(Scadent).filter(Scadent.IDScadent == IDScadent).first()
  return render_template('removescadent.html', IDMasina=IDMasina, IDScadent=IDScadent, scadent=scadent)


@scadente.route('/<email>/<IDMasina>/<IDScadent>/remove/yes',methods=['GET','POST'])
@login_required
def removeScadentYes(email, IDMasina, IDScadent):
  if email != current_user.email:
    # Forbidden, No Access
    abort(403)
  scadent = db.session.query(Scadent).filter(Scadent.IDScadent == IDScadent).first()
  db.session.delete(scadent)
  db.session.commit()
  flash("Scadentul a fost sters cu success")

  return redirect(url_for('masini.detailsVehicle', email=email, IDMasina=IDMasina))


@scadente.route('/<email>/<IDMasina>/<IDScadent>/refresh',methods=['GET','POST'])
@login_required
def refreshScadent(email, IDMasina, IDScadent):
  if email != current_user.email:
    # Forbidden, No Access
    abort(403)
  scadent = db.session.query(Scadent).filter(Scadent.IDScadent == IDScadent).first()
  return render_template('refreshscadent.html', IDMasina=IDMasina, IDScadent=IDScadent, scadent=scadent)

@scadente.route('/<email>/<IDMasina>/<IDScadent>/refresh/yes',methods=['GET','POST'])
@login_required
def refreshScadentYes(email, IDMasina, IDScadent):
  if email != current_user.email:
    # Forbidden, No Access
    abort(403)
  masina = db.session.query(Masina).filter(Masina.IDMasina == IDMasina).first()
  scadent = db.session.query(Scadent).filter(Scadent.IDScadent == IDScadent).first()

  now = datetime.datetime.now()
  scadent.dataExp = now + datetime.timedelta(int(scadent.viataZile))
  if scadent.areKM == True:
    scadent.kmExp = int(masina.kilometraj) + int(scadent.viataKm)

  db.session.commit()
  flash("Scadentul a fost reimprospatat cu success")

  return redirect(url_for('masini.detailsVehicle', email=email, IDMasina=IDMasina))
