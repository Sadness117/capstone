from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

# referenced warbler project for flask forms
class SearchPokemon(FlaskForm):
    """Form for seaching for pokemon"""

    pokemon = StringField('pokemon', validators=[DataRequired()])

class AddUser(FlaskForm):
    """Form for adding new users to the database"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=5)])
