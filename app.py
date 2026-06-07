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
            "nom": request.form["nom"],
            "primer_cognom": request.form["primer_cognom"],
            "segon_cognom": request.form["segon_cognom"],
            "edat": request.form["edat"],
            "genere": request.form["genere"]
        }
        return redirect(url_for("detail", entry_id=entry_id))
    return render_template("register.html")

@app.route("/p/<entry_id>")
def detail(entry_id):
    if entry_id not in database:
        return "Not found", 404
    return render_template("detail.html", data=database[entry_id], entry_id=entry_id)

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/search_person")
def search_person():
    cercador_persona = request.args.get("cercador_persona", "").lower()

    # Filtre simple
    if cercador_persona:

         # Recuperar totes les persones
        people = supabase.table("persons").select("*").execute().data

        people = [
            p for p in people
            if cercador_persona in p["nom"].lower()
            or cercador_persona in p["primer_cognom"].lower()
            or cercador_persona in p["segon_cognom"].lower()
            or cercador_persona in p["edat"].lower()
            or cercador_persona in p["genere"].lower()
        ]

    return render_template("search_person.html", people=people)

if __name__ == "__main__":
    app.run()