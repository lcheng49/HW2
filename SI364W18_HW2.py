## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
import requests
import json
from flask import Flask, request, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
    a_name = StringField("Enter the name of an album:", validators=[Required()])
    options = RadioField("How much do you like this album? (1 low, 3high)", choices=[('1','1'), ('2','2'), ('3','3')], validators =[Required()])
    submit = SubmitField("Submit")



####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform', methods = ['GET'])
def a_name():
    return render_template('artistform.html', artist=request.args.get('artist',''))

@app.route('/artistinfo', methods = ['GET'])
def a_info():
    a_name = request.args.get('artist','')
    para = {'term': a_name}
    base = 'https://itunes.apple.com/search'
    res = requests.get(base, params=para)
    return render_template('artist_info.html', objects = res.json()['results'])

@app.route('/artistlinks')
def a_link():
    return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>', methods = ['GET'])
def s_song(artist_name):
    para = {'term': artist_name}
    base = 'https://itunes.apple.com/search'
    res = requests.get(base, params=para)
    return render_template('specific_artist.html', results = res.json()['results'])

@app.route('/album_entry')
def a_entry():
    a_form = AlbumEntryForm()
    return render_template('album_entry.html', form=a_form)

@app.route('/album_result', methods=['POST'])
def a_result():
    form = AlbumEntryForm()
    if form.validate_on_submit():
        a_name = form.a_name.data
        a_rating = form.options.data
        return render_template('album_data.html', a_name=a_name, options = a_rating)
    flash('All fields are required!')
    return redirect(url_for('a_entry'))

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
