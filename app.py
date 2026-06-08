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
    # Obtenir totes les persones existents per omplir el selector
    people = supabase.table("persons").select("id, nom, primer_cognom").execute().data

    if request.method == "POST":

        nom = request.form["nom"]
        primer_cognom = request.form["primer_cognom"]
        segon_cognom = request.form["segon_cognom"]
        edat = request.form["edat"]
        genere = request.form["genere"]

        familiars = request.form.getlist("familiars")  # Llista d’IDs

        # 1) Inserir la persona
        result = supabase.table("persons").insert({
            "nom": nom,
            "primer_cognom": primer_cognom,
            "segon_cognom": segon_cognom,
            "edat": int(edat),
            "genere": genere,
            "familiars": familiars
        }).execute()

        new_id = result.data[0]["id"]

        # 2) RELACIÓ BIDIRECCIONAL
        # Afegir aquesta persona com a familiar dels seleccionats
        for fam_id in familiars:
            fam_data = supabase.table("persons").select("familiars").eq("id", fam_id).single().execute().data
            
            # 🔥 Convertir None → []
            llista = fam_data.get("familiars") or []

            if new_id not in llista:
                llista.append(new_id)

            supabase.table("persons").update({"familiars": llista}).eq("id", fam_id).execute()

        return redirect(f"/detail/{new_id}")

    return render_template("register.html", people=people)

@app.route("/detail/<entry_id>")
def detail(entry_id):

    persona = supabase.table("persons").select("*").eq("id", entry_id).single().execute().data

    familiars = []
    if persona.get("familiars"):
        familiars = supabase.table("persons").select("*").in_("id", persona["familiars"]).execute().data

    return render_template("detail.html", data=persona, familiars=familiars)


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