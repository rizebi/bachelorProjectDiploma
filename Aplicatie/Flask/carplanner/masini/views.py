from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import current_user, login_required

from carplanner import db, app
from carplanner.models import Masina, Marca, Scadent

from carplanner.masini.forms import AddVehicleForm, EditVehicleForm

masini = Blueprint('masini',__name__)


@masini.route('/<email>/addvehicle',methods=['GET','POST'])
@login_required
def addVehicle(email):
  app.logger.info("Am intrat in addvehicle")
  form = AddVehicleForm()
  form.modelMasina.choices = [(str(marca.IDAuto), marca.modelMasina) for marca in Marca.query.filter_by().all()]
  if form.validate_on_submit():
    app.logger.info("Am intrat in addvehicle -> validate_on_submit")
    app.logger.info("form.marcaMasina.data = " + str(form.marcaMasina.data))
    app.logger.info("form.modelMasina.data = " + str(form.modelMasina.data))
    app.logger.info("form.numarInmatriculare.data = " + form.numarInmatriculare.data)
    app.logger.info("form.kilometraj.data = " + form.kilometraj.data)
    app.logger.info("form.anFabricatie.data = " + str(form.anFabricatie.data))
    app.logger.info("form.combustibil.data = " + str(form.combustibil.data))
    app.logger.info("form.capacitateCilindrica.data = " + str(form.capacitateCilindrica.data))
    app.logger.info("form.codMotor.data = " + form.codMotor.data)
    app.logger.info("form.VIN.data = " + form.VIN.data)
    app.logger.info("form.detaliiMasina.data = " + form.detaliiMasina.data)
    app.logger.info("current_user.email = " + current_user.email)

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

    masina = Masina(current_user.IDUser, form.modelMasina.data, form.detaliiMasina.data, form.VIN.data, form.combustibil.data, form.capacitateCilindrica.data, form.anFabricatie.data, form.codMotor.data, form.numarInmatriculare.data, form.kilometraj.data, 0)
    db.session.add(masina)
    db.session.commit()
    flash("Vehicul adaugat cu succes")

    return redirect(url_for('scadente.defaultScadent', email=current_user.email, numarInmatriculare=form.numarInmatriculare.data))


  return render_template('addvehicle.html',form=form)

@masini.route('/model/<marca>')
@login_required
def model(marca):
  app.logger.info("Am intrat in model")

  modele = Marca.query.filter_by(marcaMasina = marca).all()

  modelArray = []

  for model in modele:
    modelObj = {}
    modelObj['IDAuto'] = str(model.IDAuto)
    modelObj['modelMasina'] = model.modelMasina
    modelArray.append(modelObj)

  app.logger.info(modelArray)

  return jsonify({'modele' : modelArray})



@masini.route('/<email>/<IDMasina>/details',methods=['GET','POST'])
@login_required
def detailsVehicle(email, IDMasina):

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
                     "crestereZilnica" : masina.crestereZilnica, "IDMasina" : masina.IDMasina}

  scadente = Scadent.query.filter_by(IDMasina = masina.IDMasina).order_by(Scadent.dataExp.asc()).all()




  return render_template('detailsvehicle.html', masina=masinaPregatita, scadente=scadente)


@masini.route('/<email>/<IDMasina>/edit',methods=['GET','POST'])
@login_required
def editVehicle(email, IDMasina):
  form = EditVehicleForm()


  masina = db.session.query(Masina).filter(Masina.IDMasina == IDMasina).first()

  '''choicesCombustibil = []
  choicesCombustibil.append(masina.combustibil)

  for choice in [("Benzina", "Motorina", "Electric", "Hibrid", "Benzina + GPL", "Hidrogen"]:
    if choice not in choicesCombustibil:
      choicesCombustibil.append(masina.combustibil)'''

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
    masina.kilometraj = form.kilometraj.data
    masina.anFabricatie = form.anFabricatie.data
    masina.combustibil = form.combustibil.data
    masina.capacitateCilindrica = form.capacitateCilindrica.data
    masina.codMotor = form.codMotor.data
    masina.VIN = form.VIN.data
    masina.detaliiMasina = form.detaliiMasina.data

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
  masina = db.session.query(Masina).filter(Masina.IDMasina == IDMasina).first()

  return render_template('removevehicle.html', masina=masina, IDMasina=IDMasina)


@masini.route('/<email>/<IDMasina>/remove/yes',methods=['GET','POST'])
@login_required
def removeVehicleYes(email, IDMasina):

  scadente = db.session.query(Scadent).filter(Scadent.IDMasina == IDMasina).delete()#.all()
  masina = db.session.query(Masina).filter(Masina.IDMasina == IDMasina).delete()#.first()
  flash("Masina si scadentele aferente au fost sterse cu succces")

  db.session.commit()

  return redirect(url_for('useri.userhome', email=current_user.email))


'''
# int: makes sure that the blog_post_id gets passed as in integer
# instead of a string so we can look it up later.
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    # grab the requested blog post by id number or return 404
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html',title=blog_post.title,
                            date=blog_post.date,post=blog_post
    )

@blog_posts.route("/<int:blog_post_id>/update", methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        # Forbidden, No Access
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
    return render_template('create_post.html', title='Update',
                           form=form)


@blog_posts.route("/<int:blog_post_id>/delete", methods=['POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))
'''
