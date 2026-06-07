from webbrowser import get

from supabase import create_client, Client
from flask import Flask, render_template, request, redirect, url_for

import os
import uuid

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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

@app.route("/detail/<entry_id>")
def detail(entry_id):
    if entry_id not in database:
        return "Not found", 404
    return render_template("detail.html", data=database[entry_id], entry_id=entry_id)

@app.route("/search")
def search():

    cerca_persona = get(request.args.get("cerca_persona", "")).lower()

    # Recuperar totes les persones
    people = supabase.table("persons").select("*").execute().data

    # Filtre segur
    if cerca_persona:
        people = [
            p for p in people
            if cerca_persona in p.get("nom", "").lower()
            or cerca_persona in p.get("primer_cognom", "").lower()
            or cerca_persona in p.get("segon_cognom", "").lower()
            or cerca_persona in str(p.get("edat", "")).lower()
            or cerca_persona in p.get("genere", "").lower()
        ]

    return render_template("search.html", people=people, cerca_persona=cerca_persona)


if __name__ == "__main__":
    app.run()