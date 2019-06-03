from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import current_user, login_required

from carplanner import db, app
from carplanner.models import Masina, Marca

from carplanner.masini.forms import AddVehicleForm

masini = Blueprint('masini',__name__)


@masini.route('/addvehicle',methods=['GET','POST'])
@login_required
def addVehicle():
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
    app.logger.info("form.capacitateCilindrica.data = " + str(form.capacitateCilindrica.data))
    app.logger.info("form.codMotor.data = " + form.codMotor.data)
    app.logger.info("form.VIN.data = " + form.VIN.data)
    app.logger.info("form.detaliiMasina.data = " + form.detaliiMasina.data)

  '''blog_post = BlogPost(title=form.title.data,
                     text=form.text.data,
                     user_id=current_user.id
                     )
  db.session.add(blog_post)
  db.session.commit()'''
  '''    flash("Vehicul adaugat cu succes")
  return redirect(url_for('useri.userhome', email=current_user.email))
  '''




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
