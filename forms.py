from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField
from wtforms.validators import InputRequired, Optional, URL


class AddPetForm(FlaskForm):
    """Form for adding pets."""

    name = StringField(
        "Pet Name", 
        validators=[InputRequired()]
    )

    species = SelectField(
        "Pet species",
        choices=[("cat","cat"), ("dog", "dog"), ("porcupine", "porcupine")],
        validators=[InputRequired()]
    )

    photo_url= StringField(
        "Pet photo", 
        validators=[Optional(), URL()]
    )

    age = SelectField(
        "Pet age", 
        choices=[("baby", "baby"), ("young", "young"), ("adult", "adult"), ("senior","senior")]
    )

    notes = StringField(
        "Pet notes", 
        validators=[Optional()]
    )

#########################################################################################################

class EditPetForm(FlaskForm):
    """Form for editing pets."""

    name = StringField(
        "Pet Name",
        validators=[InputRequired()]
    )

    species = SelectField(
        "Pet species", 
        choices=[("cat", "cat"), ("dog", "dog"), ("porcupine", "porcupine")],
        validators=[InputRequired()]
    )

    photo_url = StringField(
        "Pet photo", 
        validators=[Optional(), URL()]
    )

    age = SelectField(
        "Pet age", 
        choices=[("baby", "baby"), ("young", "young"), ("adult", "adult"), ("senior", "senior")]
    )

    available = BooleanField(
        "Available", 
    )

    notes = StringField(
        "Pet notes", 
        validators=[Optional()]
    )

