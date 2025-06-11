# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 05:02:01 2020

@author: roysoumy
"""
import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, send_file
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user , logout_user, login_required

posts = [
	{
                
                'author':'Soumya Roy',
                'title':'Canada FSA forecast available',
                'content': 'The forecast by fsa for all carriers is available for download now in Forecasts page.',
                'date_posted': 'May 9, 2022'
                
                },

	{
                
                'author':'Soumya Roy',
                'title':'Q1 R&O FYP Forecast now available',
                'content': 'The forecast by zip and SC-DS is available for download now in Forecasts page.',
                'date_posted': 'March 28, 2022'
                
                },

        {
                
                'author':'Soumya Roy',
                'title':'Canada FSA Sort Forecast added.',
                'content': 'The peak day Canada Sort forecast by FSA is available for download now.',
                'date_posted': 'July 30, 2021'
                
                },

        {
                
                'author':'Soumya Roy',
                'title':'Cube Forecast added.',
                'content': 'The 8-week cube forecast is available for download now.',
                'date_posted': 'June 22, 2021'
                
                },
        {
                
                'author':'Soumya Roy',
                'title':'AMZL Peak 2021 DS Forecast added.',
                'content': 'The AMZL Delivery Station volume forecast for sort centers for peak day is available to download.',
                'date_posted': 'June 7, 2021'
                
                },

        {
                
                'author':'Soumya Roy',
                'title':'Forecast Site Update',
                'content': 'Forecast is available for download in the account page after login.',
                'date_posted': 'July 22, 2020'
                
                },
        {
                
                'author':'Soumya Roy',
                'title':'Forecast Site Update',
                'content': 'Demand and DDU Forecast model is ready to deploy',
                'date_posted': 'July 7, 2020'
                
                },
        {
                
                'author':'Soumya Roy',
                'title':'Forecast Site Launched',
                'content': 'Launched site for forecasting as a service platform',
                'date_posted': 'June 26, 2020'
                
                }
                
        
        
        ]

###Creating the home page - thats what route does
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts = posts)

@app.route("/about")
def about():
    return render_template('about.html', title = 'About')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)


@app.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title = 'Login', form = form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    
    return picture_fn


@app.route("/account", methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename= 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file=image_file, form=form)

@app.route('/download')
def download_file():
	#path = "html2pdf.pdf"
	#path = "info.xlsx"
	path = "/local/home/roysoumy/Flask_Blog/flaskblog/static/Zip_level_forecast_8_weeks.txt"
	#path = "sample.txt"
	return send_file(path, as_attachment=True)


@app.route('/download2')
def download_file2():
	#path = "html2pdf.pdf"
	#path = "info.xlsx"
	path = "/local/home/roysoumy/Flask_Blog/flaskblog/static/Zip_level_forecast_16_weeks.txt"
	#path = "sample.txt"
	return send_file(path, as_attachment=True)

@app.route('/download3')
def download_file3():
	#path = "html2pdf.pdf"
	#path = "info.xlsx"
	path = "/local/home/roysoumy/Flask_Blog/flaskblog/static/AMZL DS Forecast.txt"
	#path = "sample.txt"
	return send_file(path, as_attachment=True)


@app.route('/download4')
def download_file4():
	#path = "html2pdf.pdf"
	#path = "info.xlsx"
	path = "/local/home/roysoumy/Flask_Blog/flaskblog/static/q2_rno_ddu_peak_day_zip_volume.txt"
	#path = "sample.txt"
	return send_file(path, as_attachment=True)

@app.route('/download5')
def download_file5():
	#path = "html2pdf.pdf"
	#path = "info.xlsx"
	path = "/local/home/roysoumy/Flask_Blog/flaskblog/static/q2_rno_AMZL_sc_ds_peak_day_forecast.txt"
	#path = "sample.txt"
	return send_file(path, as_attachment=True)

@app.route('/download6')
def download_file6():
	#path = "html2pdf.pdf"
	#path = "info.xlsx"
	path = "/local/home/roysoumy/Flask_Blog/flaskblog/static/Package_size_cube_forecast.txt"
	#path = "sample.txt"
	return send_file(path, as_attachment=True)

@app.route('/download7')
def download_file7():
	#path = "html2pdf.pdf"
	#path = "info.xlsx"
	path = "/local/home/roysoumy/Flask_Blog/flaskblog/static/Canada_Sort_SC_FSA_Forecast_peak_day_2021.txt"
	#path = "sample.txt"
	return send_file(path, as_attachment=True)

@app.route('/download8')
def download_file8():
	#path = "html2pdf.pdf"
	#path = "info.xlsx"
	path = "/local/home/roysoumy/Flask_Blog/flaskblog/static/q2_rno_ddu_full_year_zip_volume.txt"
	#path = "sample.txt"
	return send_file(path, as_attachment=True)



@app.route('/download9')
def download_file9():
	#path = "html2pdf.pdf"
	#path = "info.xlsx"
	path = "/local/home/roysoumy/Flask_Blog/flaskblog/static/q1_rno_AMZL_sc_ds_full_year_forecast.txt"
	#path = "sample.txt"
	return send_file(path, as_attachment=True)


@app.route('/download10')
def download_file10():
	#path = "html2pdf.pdf"
	#path = "info.xlsx"
	path = "/local/home/roysoumy/Flask_Blog/flaskblog/static/canada_mid_term_fsa_forecast.txt"
	#path = "sample.txt"
	return send_file(path, as_attachment=True)


