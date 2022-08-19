from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import http.client
import requests

auth = Blueprint('auth', __name__)

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
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)

@auth.route('/url_shortener', methods = ['POST', 'GET'])
#@login_required
def url_shortener():
    if request.method == 'POST':
        site = request.form['url']

        if 'https://' not in site:
            site = "https://" + site

        payload = 'url=' + site
        conn = http.client.HTTPSConnection("url-shortener-service.p.rapidapi.com")
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'X-RapidAPI-Key': "8981923446msh8c91295000d75e5p1e8de0jsn7c06af14c53a",
            'X-RapidAPI-Host': "url-shortener-service.p.rapidapi.com"
        }
        conn.request("POST", "/shorten", payload, headers)
        res = conn.getresponse()
        data = res.read()
        flash('Shortened URL created!', category='success')
        print(site)
        print(payload)
        print(data.decode("utf-8"))
        final=data.decode("utf-8")
        final = final.replace('"result_url":','')
        final = final.replace('"','')
        final = final.replace('{','')
        final = final.replace('}','')
        print(final)
        return render_template('url_shortener.html', result=final, user=current_user )

    else:
        return render_template('url_shortener.html',user=current_user, )

@auth.route('/weather', methods = ['POST', 'GET'])
def weather():
    if request.method == 'POST':
        try:
            city = request.form['city']
            response = requests.get("http://api.weatherapi.com/v1/current.json?key=d611d4fc42174c24ba6222614222207&q="+city+"&aqi=no")
            data = response.json()
            print(data)
            weatherDesc = data["current"]["condition"]["text"]
            c = data["current"]["temp_c"]
            f = data["current"]["temp_f"]
            t = data["location"]["localtime"]
            n = data["location"]["name"]
            i = data["current"]["condition"]["icon"]
            return render_template('weather.html', name=n, icon=i, result = weatherDesc, city = city, Faren=f, Celsius = c, time=t, user=current_user )
        except:
            e = "Could not find the location."
            return render_template('weather.html', exception=e, user=current_user, )

    else:
        return render_template('weather.html',user=current_user, )

@auth.route('/airport', methods = ['POST', 'GET'])
def weather():
    if request.method == 'POST':
        try:
            airport = request.form['aiport']
            response = requests.get("http://api.weatherapi.com/v1/current.json?key=d611d4fc42174c24ba6222614222207&q="+city+"&aqi=no")
            data = response.json()
            return render_template('airport.html', user=current_user )
        except:
            e = "Could not find the Airport."
            return render_template('airport.html', exception=e, user=current_user, )

    else:
        return render_template('weather.html',user=current_user, )       
