from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , SelectField, URLField, TimeField
from wtforms.validators import DataRequired,URL
import csv



app = Flask(__name__)
app.config['SECRET_KEY'] = '8'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Cafe Location', validators=[DataRequired(), URL()])
    openTime = StringField('Open Time eg:9:00 AM', validators=[DataRequired()])
    closeTime = StringField('Close Time eg: 9:30 PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee rating', choices=['✘', '☕', '☕☕', '☕☕☕', '☕☕☕☕',
                                                           '☕☕☕☕☕'], validators=[DataRequired()])
    wifi_rating = SelectField('Wifi rating',choices=['✘', '💪', '💪💪', '💪💪💪','💪💪💪💪',
                                                    '💪💪💪💪💪'], validators=[DataRequired()])
    power_rating = SelectField('Power rating', choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌',
                                                     '🔌🔌🔌🔌🔌'], validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open(file="cafe-data.csv", mode="a", newline='', encoding="utf-8") as file:
            new_list=[]
            new_list = [form.cafe.data, form.location.data, form.openTime.data,form.closeTime.data,form.coffee_rating.data,
                       form.wifi_rating.data, form.power_rating.data]
            writes = csv.writer(file)
            writes.writerow(new_list)
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
