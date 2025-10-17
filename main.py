from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
# Initialise the SQLAlchemy extension
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CREATE TABLE
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    # Method to turn the object into a dictionary
    def to_dict(self):
        # Use a dictionary comprehension to create a dict of all columns
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# Create tables if they don't exist
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Get a random cafe
@app.route("/random")
def get_random_cafe():
    # Execute a select statement to get all cafes
    result = db.session.execute(db.select(Cafe))
    # Scalar to return objects, all() to get a list
    all_cafes = result.scalars().all()
    # Choose a random cafe from the list
    random_cafe = random.choice(all_cafes)
    # Return the chosen cafe as a JSON response
    return jsonify(cafe=random_cafe.to_dict())


# HTTP GET - Get all cafes
@app.route("/all")
def get_all_cafes():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    # Return a JSON list of all cafes
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


# HTTP GET - Search for cafes by location
@app.route("/search")
def get_cafe_at_location():
    # Get location from query parameter, e.g., /search?loc=Peckham
    query_location = request.args.get("loc")
    # Select cafes where location matches the query
    result = db.session.execute(
        db.select(Cafe).where(Cafe.location == query_location))
    # Note, this may get more than one cafe per location
    all_cafes = result.scalars().all()
    if all_cafes:
        # Return list of cafes found
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        # Return 404 error if no cafes are found
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404


# HTTP POST - Add a new cafe (requires POST request with form data)
@app.route("/add", methods=["POST"])
def post_new_cafe():
    # Create a new Cafe object from the form data
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        # Form values are strings, so convert to boolean
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


# HTTP PATCH - Update the coffee price of a cafe by ID
# Example: http://127.0.0.1:5000/update-price/CAFE_ID?new_price=£5.67
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_new_price(cafe_id):
    # Get new price from query parameter
    new_price = request.args.get("new_price")
    # Get cafe by its primary key
    cafe = db.session.get(entity=Cafe, ident=cafe_id)
    if cafe:
        # Update the price and commit the changes
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200
    else:
        # Return 404 if cafe not found
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


# HTTP DELETE - Delete a cafe with a particular id. Requires a secret api-key.
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    # Get api-key from query parameter
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        # Get cafe by its primary key
        # FIX: Changed to db.session.get(Cafe, cafe_id) to correctly fetch the object.
        cafe = db.session.get(Cafe, cafe_id)

        if cafe:
            # Delete the cafe and commit the changes
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            # Return 404 if cafe not found
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        # Return 403 Forbidden if api-key is incorrect
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


if __name__ == '__main__':
    app.run(debug=True)