from flask import Flask, redirect, render_template
from models import Pet, db, connect_db
from flask_debugtoolbar import DebugToolbarExtension
from forms import AddPetForm, EditPetForm


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
        pet.age = form.age.data
        pet.notes = form.notes.data

        db.session.commit()
        return redirect("/")

    else:
        return render_template("pet_edit_form.html", form=form)


