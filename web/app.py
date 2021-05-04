from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import json


app = Flask(__name__, template_folder='.')

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'secret_key_lkjbdsfasojabdl'

# Flask-Bootstrap requires this line
Bootstrap(app)

class IdentifiersForm(FlaskForm):
    id1 = StringField('Sensor 1 ID')
    id2 = StringField('Sensor 2 ID')
    id3 = StringField('Sensor 3 ID')
    id4 = StringField('Sensor 4 ID')
    id5 = StringField('Sensor 5 ID')
    id6 = StringField('Sensor 6 ID')
    id7 = StringField('Sensor 7 ID')
    id8 = StringField('Sensor 8 ID')
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    # TODO: populate form with data from config file
    form = IdentifiersForm()
    identifiers = {}
    if form.validate_on_submit():
        identifiers = {
            'id1': form.id1.data,
            'id2': form.id2.data,
            'id3': form.id3.data,
            'id4': form.id4.data,
            'id5': form.id5.data,
            'id6': form.id6.data,
            'id7': form.id7.data,
            'id8': form.id8.data,
        }
    
    # TODO: write config to file

    j = json.dumps(identifiers)
    return render_template('index.html', form=form, json=j)

if __name__ == '__main__':
    app.run()