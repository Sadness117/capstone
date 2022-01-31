from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connects database"""

    db.app = app
    db.init_app(app)



# used some code from warbler project from springboard
class User(db.Model):
    """User for the pokedex"""

    __tablename__ = 'Pokemon_user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.Text,nullable=False,unique=True)
    password = db.Column(db.Text,nullable=False)


    @classmethod
    def signup(cls, username, password):
        """Signup for the user"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(username=username,password=hashed_pwd)
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """finds the user and checks if its correct"""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class FavoritePokemon(db.Model):
    __tablename__ = 'Favorite_pokemon'

    id = db.Column(db.Integer,primary_key=True)
    pokemon_name = db.Column(db.Text,nullable=False)
    poke_id = db.Column(db.Integer,nullable=False, unique = True)
    pokemon_link = db.Column(db.Text,nullable=False)
    pokemon_img = db.Column(db.Text,nullable=False)
    poke_user = db.Column(
        db.Integer,
        db.ForeignKey('Pokemon_user.id', ondelete='CASCADE'),
        nullable=False,
    )

    user = db.relationship('User')