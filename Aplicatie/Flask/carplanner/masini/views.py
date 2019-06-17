from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify, abort
from flask_login import current_user, login_required

from carplanner import db, app
from carplanner.models import Masina, Marca, Scadent
from carplanner.masini.forms import AddVehicleForm, EditVehicleForm
import datetime
import math

masini = Blueprint('masini',__name__)


@masini.route('/<email>/addvehicle',methods=['GET','POST'])
@login_required
def addVehicle(email):
  if email != current_user.email:
    # Forbidden, No Access
    abort(403)
  form = AddVehicleForm()
  marci = db.session.query(Marca.marcaMasina).distinct(Marca.marcaMasina).all()

  marcaChoices = []
  for marca in marci:
    marcaChoices.append((marca[0], marca[0]))

  form.modelMasina.choices = [(str(marca.IDAuto), marca.modelMasina) for marca in Marca.query.filter_by().all()]
  form.marcaMasina.choices = marcaChoices

  now = datetime.datetime.now()


  if form.validate_on_submit():

    if form.anFabricatie.data == "":
      form.anFabricatie.data = 0
    if form.capacitateCilindrica.data == "":
      form.capacitateCilindrica.data = 0
    if form.codMotor.data == "":
      form.codMotor.data = " "
    if form.VIN.data == "":
      form.VIN.data = " "
    if form.detaliiMasina.data == "":
      form.detaliiMasina.data = " "

    masina = Masina(current_user.IDUser, form.modelMasina.data, form.detaliiMasina.data, form.VIN.data, form.combustibil.data, form.capacitateCilindrica.data, form.anFabricatie.data, form.codMotor.data, form.numarInmatriculare.data, form.kilometraj.data, 0, now)
    db.session.add(masina)
    db.session.commit()
    flash("Vehicul adaugat cu succes")

    return redirect(url_for('scadente.defaultScadent', email=current_user.email, numarInmatriculare=form.numarInmatriculare.data))


  return render_template('addvehicle.html',form=form)

@masini.route('/model/<marca>')
@login_required
def model(marca):

  modele = Marca.query.filter_by(marcaMasina = marca).all()

  modelArray = []

  for model in modele:
    modelObj = {}
    modelObj['IDAuto'] = str(model.IDAuto)
    modelObj['modelMasina'] = model.modelMasina
    modelArray.append(modelObj)

  return jsonify({'modele' : modelArray})



@masini.route('/<email>/<IDMasina>/details',methods=['GET','POST'])
@login_required
def detailsVehicle(email, IDMasina):
  if email != current_user.email:
    # Forbidden, No Access
    abort(403)
  masina, marca = db.session.query(Masina, Marca).filter(Masina.IDAuto == Marca.IDAuto, Masina.IDMasina == IDMasina).first()
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

  masinaPregatita = {"marcaMasina" : marca.marcaMasina, "modelMasina" : marca.modelMasina,
                     "numarInmatriculare" : masina.numarInmatriculare, "kilometraj" : masina.kilometraj,
                     "scadentData" : scadentMaximDateAfis, "scadentKm" : scadentMaximKmAfis,
                     "detaliiMasina" : masina.detaliiMasina, "VIN" : masina.VIN,
                     "combustibil" : masina.combustibil, "capacitateCilindrica" : masina.capacitateCilindrica,
                     "anFabricatie" : masina.anFabricatie, "codMotor" : masina.codMotor,
                     "crestereZilnica" : masina.crestereZilnica, "IDMasina" : masina.IDMasina, "lastUpdate" : masina.lastUpdate}

  scadente = Scadent.query.filter_by(IDMasina = masina.IDMasina).order_by(Scadent.dataExp.asc()).all()




  return render_template('detailsvehicle.html', masina=masinaPregatita, scadente=scadente)


@masini.route('/<email>/<IDMasina>/edit',methods=['GET','POST'])
@login_required
def editVehicle(email, IDMasina):
  if email != current_user.email:
    # Forbidden, No Access
    abort(403)
  form = EditVehicleForm()
  masina = db.session.query(Masina).filter(Masina.IDMasina == IDMasina).first()

  if form.validate_on_submit():

    if form.anFabricatie.data == "":
      form.anFabricatie.data = 0
    if form.capacitateCilindrica.data == "":
      form.capacitateCilindrica.data = 0
    if form.codMotor.data == "":
      form.codMotor.data = " "
    if form.VIN.data == "":
      form.VIN.data = " "
    if form.detaliiMasina.data == "":
      form.detaliiMasina.data = " "

    masina.numarInmatriculare = form.numarInmatriculare.data
    masina.anFabricatie = form.anFabricatie.data
    masina.combustibil = form.combustibil.data
    masina.capacitateCilindrica = form.capacitateCilindrica.data
    masina.codMotor = form.codMotor.data
    masina.VIN = form.VIN.data
    masina.detaliiMasina = form.detaliiMasina.data

    if masina.kilometraj != form.kilometraj.data:
      # We must update the lastUpdate and crestereZilnica
      now = datetime.datetime.now().date()
      daysBetween = (now - masina.lastUpdate).days
      if daysBetween != 0:
        crestereNoua = math.floor((int(form.kilometraj.data) - masina.kilometraj) / daysBetween)
        if crestereNoua <= 0:
          masina.crestereZilnica = 0
        else:
          masina.crestereZilnica = crestereNoua
      else:
        masina.crestereZilnica = int(form.kilometraj.data) - masina.kilometraj

      masina.kilometraj = form.kilometraj.data
      masina.lastUpdate = now

    db.session.commit()
    flash("Vehicul editat cu succes")

    return redirect(url_for('useri.userhome', email=current_user.email))

  elif request.method == 'GET':
    form.numarInmatriculare.data = masina.numarInmatriculare
    form.kilometraj.data = masina.kilometraj
    form.combustibil.data = masina.combustibil

    if masina.anFabricatie == "0" or masina.anFabricatie == 0:
      form.anFabricatie.data = ""
    else:
      form.anFabricatie.data = masina.anFabricatie

    if masina.capacitateCilindrica == "0" or masina.capacitateCilindrica == 0:
      form.capacitateCilindrica.data = ""
    else:
      form.capacitateCilindrica.data = masina.capacitateCilindrica

    if masina.codMotor == " ":
      form.codMotor.data = ""
    else:
      form.codMotor.data = masina.codMotor

    if masina.VIN == " ":
      form.VIN.data = ""
    else:
      form.VIN.data = masina.VIN

    if masina.detaliiMasina == " ":
      form.detaliiMasina.data = ""
    else:
      form.detaliiMasina.data = masina.detaliiMasina


  return render_template('editvehicle.html', form=form, email=email, IDMasina=IDMasina)




@masini.route('/<email>/<IDMasina>/remove',methods=['GET','POST'])
@login_required
def removeVehicle(email, IDMasina):
  if email != current_user.email:
    # Forbidden, No Access
    abort(403)
  masina = db.session.query(Masina).filter(Masina.IDMasina == IDMasina).first()

  return render_template('removevehicle.html', masina=masina, IDMasina=IDMasina)


@masini.route('/<email>/<IDMasina>/remove/yes',methods=['GET','POST'])
@login_required
def removeVehicleYes(email, IDMasina):
  if email != current_user.email:
    # Forbidden, No Access
    abort(403)
  scadente = db.session.query(Scadent).filter(Scadent.IDMasina == IDMasina).delete()#.all()
  masina = db.session.query(Masina).filter(Masina.IDMasina == IDMasina).delete()#.first()
  flash("Masina si scadentele aferente au fost sterse cu succces")

  db.session.commit()

  return redirect(url_for('useri.userhome', email=current_user.email))
