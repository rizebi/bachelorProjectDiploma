from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required

from carplanner import db, app
from carplanner.models import Scadent, Masina, RevizieDefault
from carplanner.scadente.forms import DefaultScadentForm, AddScadentForm, EditScadentForm
import datetime

scadente = Blueprint('scadente',__name__)


@scadente.route('/<email>/<numarInmatriculare>/defaultscadent',methods=['GET','POST'])
@login_required
def defaultScadent(email, numarInmatriculare):

  now = datetime.datetime.now()
  form = DefaultScadentForm()

  if form.validate_on_submit():
    app.logger.info("Am intrat in defaultScadent -> validate_on_submit")
    app.logger.info("form.default1.data = " + str(form.default1.data))
    app.logger.info("form.default2.data = " + str(form.default2.data))
    app.logger.info("form.default3.data = " + str(form.default3.data))
    app.logger.info("form.default4.data = " + str(form.default4.data))
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

  scadent = db.session.query(Scadent).filter(Scadent.IDScadent == IDScadent).first()
  return render_template('removescadent.html', IDMasina=IDMasina, IDScadent=IDScadent, scadent=scadent)

@scadente.route('/<email>/<IDMasina>/<IDScadent>/remove/yes',methods=['GET','POST'])
@login_required
def removeScadentYes(email, IDMasina, IDScadent):

  scadent = db.session.query(Scadent).filter(Scadent.IDScadent == IDScadent).first()
  db.session.delete(scadent)
  db.session.commit()
  flash("Scadentul a fost sters cu success")

  return redirect(url_for('masini.detailsVehicle', email=email, IDMasina=IDMasina))




'''
@scadente.route('/create',methods=['GET','POST'])

@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():

        blog_post = BlogPost(title=form.title.data,
                             text=form.text.data,
                             user_id=current_user.id
                             )
        db.session.add(blog_post)
        db.session.commit()
        flash("Blog Post Created")
        return redirect(url_for('core.index'))

    return render_template('create_post.html',form=form)


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
