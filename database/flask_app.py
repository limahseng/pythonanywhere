from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username=<your_username>,
    password=<your_password>,
    hostname="<your_username>.mysql.pythonanywhere-services.com",
    databasename="<your_databasename>",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

db = SQLAlchemy(app)

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    price = db.Column(db.Float())

@app.route("/", methods=["GET", "POST"])
def index():
    bought = ""
    total = 0.0
    if request.method == "POST":
        if request.form.get('cost') == "How much?": # compute total cost
            items = request.form.getlist("items")
            for fid in items:
                item = Food.query.filter_by(id=int(fid)).first()
                bought += item.name + " @ $" + str(item.price) + "<br />"
                total += float(item.price)
        if request.form.get('insert') == "Add!": # insert new food item
            food = Food(name=request.form.get("item"), price=request.form.get("price"))
            db.session.add(food)
            db.session.commit()
    return render_template("main_page.html", foods=Food.query.all(), bought=bought, result=total)
