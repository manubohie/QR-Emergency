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

        nom = request.form["nom"]
        primer_cognom = request.form["primer_cognom"]
        segon_cognom = request.form["segon_cognom"]
        edat = request.form["edat"]
        genere = request.form["genere"]

        # Inserció real a Supabase
        result = supabase.table("persons").insert({
            "nom": nom,
            "primer_cognom": primer_cognom,
            "segon_cognom": segon_cognom,
            "edat": int(edat),
            "genere": genere
        }).execute()

        new_id = result.data[0]["id"]

        return redirect(f"/detail/{new_id}")

    return render_template("register.html")

@app.route("/detail/<entry_id>")
def detail(entry_id):

    result = supabase.table("persons").select("*").eq("id", entry_id).single().execute()

    if result.data is None:
        return "Not found", 404

    return render_template("detail.html", data=result.data)

@app.route("/search")
def search():

    cerca_persona = request.args.get("cerca_persona", "").lower()

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

        # 🔥 Si només hi ha un resultat → redirigir directament
        if len(people) == 1:
            return redirect(f"/detail/{people[0]['id']}")

    return render_template("search.html", people=people, cerca_persona=cerca_persona)


if __name__ == "__main__":
    app.run()