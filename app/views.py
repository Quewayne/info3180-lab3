"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""
import os
import smtplib
from app import app
from flask import render_template, request, redirect, url_for
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from random import randint
from wtforms import StringField, TextAreaField, SubmitField, FileField, RadioField, HiddenField
from wtforms.validators import Required, NumberRange, Email

app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)

message = """From: {} <{}>
To: {} <{}>
Subject: {}

{}
""" 


class ConForm(Form):
    name = StringField('Please enter your full name', validators=[Required()])
    email = StringField('Please enter your e-mail address', validators=[Required(),Email()])
    subject = StringField('Subject', validators=[Required()])
    msg = TextAreaField('Please enter the message you want to send.', validators=[Required()])
    submit = SubmitField('Send')
    
def sendmsg(subject,msg,toaddr,fromname):
	fromaddr  = 'qgrant96@gmail.com'
	toname = 'Cooze'
	#subject = request.form.subject.data
    	#msg = request.form.msg.data
    	#toaddr  = request.form.email.data
	#fromname = request.form.name.data
	messagetosend = message.format(
                             	fromname,
                             	fromaddr,
                             	toname,
                             	toaddr,
                             	subject,
                             	msg)

	# Credentials (if needed)
	username = 'qgrant96@gmail.com'
	password = 'coozeman11'
	#password = '{youremailapppassword}''
	# The actual mail send
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	#server.login(username)
	server.login(username,password)
	server.sendmail(fromaddr, toaddr, messagetosend)
	server.quit()


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')
    
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Render the website's contact page."""
    form=ConForm()
    
    if form.validate_on_submit():
    	#sendmsg('Test','Hello Cooze','quewayne.grant@yahoo.com','Quewayne')
    	sendmsg(form.subject.data,form.msg.data,form.email.data,form.name.data)
    	#if request.method== 'POST':
    		   		
    return render_template('contact.html',form=form)



###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
