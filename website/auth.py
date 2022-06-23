from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

#The functions contained in this file are login, logout, signup, and url shortener (added on 6/22)
#url shortner function added (line 68), planning to add the option to the navbar upon user login


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist!', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash("First name must be greater than 1 character.", category='error')
        elif password1 != password2:
            flash('Your passwords must match.', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 6 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)

@auth.route('/url-shortener')
@login_required #have the url shortener feature be available once they log in
def url_shortener():

    site = input(str())  # Have user put in the URL they want to shorten, not sure how to go about this
    conn = http.client.HTTPSConnection("url-shortener-service.p.rapidapi.com")
    payload = "url={}".format(site)

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'X-RapidAPI-Key': "8981923446msh8c91295000d75e5p1e8de0jsn7c06af14c53a",
        'X-RapidAPI-Host': "url-shortener-service.p.rapidapi.com"
    }

    conn.request("POST", "/shorten", payload, headers)

    res = conn.getresponse()
    data = res.read()
    if data.decode("utf-8"):
        flash('Shortened URL created!', category='success')
        return data.decode("utf-8")
    else:
        pass
