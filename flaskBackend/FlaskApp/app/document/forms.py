"""
Desc: Flask-WTF extension uses Python classes to represent web forms
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField

class DocumentForm(FlaskForm):
    submit = SubmitField('Upload')
