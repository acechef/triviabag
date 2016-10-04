from flask_wtf import Form
from wtforms import TextAreaField, SubmitField, StringField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, URL
from ..models import Category, User


class EditProfileForm(Form):
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class CategoryForm(Form):
    name = StringField('Name')
    submit = SubmitField('Submit')


class WebsiteForm(Form):
    url = StringField('Url', validators=[DataRequired(), Length(1, 64), URL()])
    title = StringField('Title')
    description = TextAreaField('Description')
    category = SelectField('Category', coerce=int)
    status = RadioField('Status', coerce=int,
                        choices=[(0, 'private'), (1, 'public')], default=0)
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(WebsiteForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.filter_by(user_id=user.id, is_del=0).all()]
