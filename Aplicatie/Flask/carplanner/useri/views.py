from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from carplanner import db
from werkzeug.security import generate_password_hash,check_password_hash
from carplanner.models import User
from carplanner.useri.forms import RegistrationForm, LoginForm, UpdateUserForm
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

        if user.check_password(form.parola.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Autentificare reusita!')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)
    return render_template('login.html', form=form)




@useri.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.index'))



@useri.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        print(form)
        if form.picture.data:
            email = current_user.email
            pic = add_profile_pic(form.picture.data, email)
            current_user.profile_image = pic

        current_user.email = form.email.data
        current_user.numeUser = form.numeUser.data
        current_user.prenumeUser = form.prenumeUser.data
        current_user.numeCompanie = form.numeCompanie.data

        db.session.commit()
        flash('Datele contului au fost actualizate cu succes.')
        return redirect(url_for('useri.account'))

    elif request.method == 'GET':
        form.email.data = current_user.email
        form.numeUser.data = current_user.numeUser
        form.prenumeUser.data = current_user.prenumeUser
        form.numeCompanie.data = current_user.numeCompanie

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)

'''
@useri.route("/<username>")
def user_cars(email):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
'''
