from flask import Flask, render_template, request, redirect, url_for
import uuid

app = Flask(__name__)

database = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        entry_id = str(uuid.uuid4())[:8]
        database[entry_id] = {
            "name": request.form["name"],
            "vehicle": request.form["vehicle"],
            "gender": request.form["gender"],
            "emergency_phone": request.form["emergency_phone"],
            "optional_phone": request.form["optional_phone"],
            "occupation": request.form["occupation"],
            "address": request.form["address"],
            "blood": request.form["blood"],
            "medical": request.form["medical"]
        }
        return redirect(url_for("detail", entry_id=entry_id))
    return render_template("register.html")

@app.route("/scan")
def scan():
    return render_template("scan.html")

@app.route("/p/<entry_id>")
def detail(entry_id):
    if entry_id not in database:
        return "Not found", 404
    return render_template("detail.html", data=database[entry_id], entry_id=entry_id)

if __name__ == "__main__":
    app.run()