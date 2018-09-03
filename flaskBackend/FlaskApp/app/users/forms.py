from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User, Group


class EditProfileForm(FlaskForm):
    # no changing of username for now cause groups are gonna be based on that
    # username = StringField('Username', validators=[DataRequired()])
    firstname = TextAreaField('Name', validators=[Length(min=0, max=20)])
    surname = TextAreaField('Surname', validators=[Length(min=0, max=40)])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    status = TextAreaField('Current status', validators=[Length(min=0, max=50)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username


class GroupForm(FlaskForm):
    name = StringField('Choose a name', validators=[DataRequired("Please enter a name for your group"),
                                                    Length(3, 64,
                                                           message="Must be at least 3 characters long")])
    submit = SubmitField('Create')

    def validate_username(self, name_field):
        if Group.query.filter_by(name=name_field.data).first():
            raise ValidationError('This group name is already taken.')

class MemberForm(FlaskForm):
    username = StringField('Enter username', validators=[DataRequired("Please enter the name of the user you want to add."),
                                                    Length(3, 80,
                                                           message="Must be at least 3 characters long")])
    groupname = StringField('Enter group name', validators=[DataRequired("Please enter a group name!"),  Length(3, 64,
                                                           message="Must be at least 3 characters long")])
    submit = SubmitField('Add')