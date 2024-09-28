from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , FloatField
from wtforms.validators import DataRequired
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

class MovieForm(FlaskForm):
    new_rating = FloatField("rating",validators=[DataRequired()])
    new_review = StringField("review",validators=[DataRequired()])
    done = SubmitField("Done")

# CREATE DB


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db.init_app(app)

# CREATE TABLE
class Movies(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True , nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(Float,nullable=False)
    ranking: Mapped[int] = mapped_column(nullable=False)
    review: Mapped[str] = mapped_column(nullable=False)
    img_url: Mapped[str] = mapped_column(nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    result = db.session.execute(db.select(Movies))
    all_movies = result.scalars()
    return render_template("index.html", movies=all_movies)


@app.route("/edit",methods=["GET","POST"])
def edit():
    form = MovieForm()
    edit_id = request.args.get("movie_id")
    movie_to_update = db.get_or_404(Movies, edit_id)
    if form.validate_on_submit():
        movie_to_update.rating = form.new_rating.data
        movie_to_update.review = form.new_review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=form, movie=movie_to_update)

@app.route("/delete")
def delete():
    delete_id = request.args.get("movie_id")
    movie_to_delete = db.get_or_404(Movies,delete_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
