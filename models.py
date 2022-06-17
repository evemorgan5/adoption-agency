from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://t3.ftcdn.net/jpg/03/46/83/96/360_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg"

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Pet(db.Model):
    """Pet properties"""

    __tablename__ = "pets"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(
        db.String(50),
        nullable=False
    )

    species = db.Column(
        db.String(30),
        nullable=False
    )

    photo_url = db.Column(
        db.Text,
        nullable=False, 
        default=DEFAULT_IMAGE_URL
    )

    age = db.Column(
        db.String(10), 
        nullable=False
    )

    notes = db.Column(
        db.Text, 
        nullable=False,
        default=''
    )

    available = db.Column(
        db.Boolean, 
        nullable=False, 
        default=True
    )
