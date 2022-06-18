from flask import Flask, redirect, render_template
import requests
from models import Pet, db, connect_db, DEFAULT_IMAGE_URL
from flask_debugtoolbar import DebugToolbarExtension
from forms import AddPetForm, EditPetForm
import os

PET_FINDER_API_KEY=os.environ['PET_FINDER_API_KEY']
PET_FINDER_SECRET_KEY=os.environ['PET_FINDER_SECRET_KEY']

auth_token = None

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


# debug tool bar
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
# look into line below - Eve
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
db.create_all()


@app.get("/")
def homepage():
    """Takes user to homepage
        - Shows the list of available pets
    """

    pets = Pet.query.all()
    return render_template("homepage.html", pets=pets)


@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """ For GET request
        - Shows the form fields to add a pet
        For POST request
        - Saves the pet into the database
    """

    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        photo_url = str(photo_url) if photo_url else None
        age = form.age.data
        notes = form.notes.data

        pet = Pet(
            name=name,
            species=species,
            photo_url=photo_url,
            age=age,
            notes=notes
        )

        db.session.add(pet)
        db.session.commit()
        return redirect("/")

    else:
        return render_template("pet_add_form.html", form=form)


@app.route("/<int:id>", methods=["GET", "POST"])
def edit_pet(id):
    """ For GET request,
        - Gets pet instance based on pet id
        - Shows form fields to edit a pet
        For POST request,
        - Updates and saves the pet in the database
    """

    pet = Pet.query.get_or_404(id)
    form = EditPetForm(obj = pet)

    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.photo_url = form.photo_url.data
        pet.photo_url = str(pet.photo_url) if pet.photo_url else DEFAULT_IMAGE_URL
        pet.age = form.age.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()
        return redirect("/")

    else:
        return render_template("pet_edit_form.html", form=form)



@app.before_first_request
def refresh_credentials():
    """Just once, get token and store it globally."""
    global auth_token
    auth_token = update_auth_token_string()

def update_auth_token_string():
    response=requests.get("https://api.petfinder.com/v2/oauth2/token",
    params={"{CLIENT-ID}":PET_FINDER_API_KEY, "{CLIENT-SECRET}":PET_FINDER_SECRET_KEY})
    data = response.json()
    token = data["access_token"]
    return token



