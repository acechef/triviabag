from flask_wtf import Form
from wtforms import TextAreaField, SubmitField


class EditProfileForm(Form):
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
