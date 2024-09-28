import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean


app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
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

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def cafe_random():
    cafe_data = db.session.execute(db.select(Cafe)).scalars().all()
    random_cafe = random.choice(cafe_data)
    return jsonify(cafe=random_cafe.to_dict())

@app.route("/all")
def cafe_all():
    cafe_data = db.session.execute(db.select(Cafe)).scalars().all()
    return jsonify(cafe=[cafe.to_dict() for cafe in cafe_data])

@app.route("/search")
def cafe_search():
    cafe_location = request.args.get("loc")
    cafe_data = db.session.execute(db.select(Cafe).where(Cafe.location==cafe_location)).scalars().all()
    if cafe_data:
      return jsonify(cafe=[cafe.to_dict() for cafe in cafe_data])
    else:
        return jsonify({"error":"Sorry , We dont have a cafe at requested location. "}),404




# HTTP POST - Create Record
@app.route("/add",methods=["POST"])
def cafe_add():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"Success": "Successfully added the new cafe"})


# HTTP PUT/PATCH - Update Record
@app.route("/update_price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    result=db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
    if result:
        result.coffee_price = request.args.get("new_price")
        db.session.commit()
        return jsonify(response={"success": "Price update sucessfully"})
    else:
        return jsonify({"error": "the enter id not found"}), 404


# HTTP DELETE - Delete Record
@app.route("/report_closed/<cafe_id>",methods=["DELETE"])
def delete_cafe(cafe_id):
    result = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
    if result:
        API_KEY = "Niha"
        if API_KEY == request.args.get("api_key"):
            db.session.delete(result)
            db.session.commit()
            return jsonify(response={"success": "Cafe is deleted successfully"}),200
        else:
            return jsonify({"error": "Action is not allowed"}), 404
    return jsonify({"error": "cafe is not available"}), 400




if __name__ == '__main__':
    app.run(debug=True)
