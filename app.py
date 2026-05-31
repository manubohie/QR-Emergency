from flask import Flask, render_template, request, redirect
from supabase import create_client, Client
import os
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Flask ---
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nom = request.form.get("nom")
        cognoms = request.form.get("cognoms")
        edat = request.form.get("edat")
        tipus = request.form.get("tipus")
        malalties = request.form.get("malalties")
        notes = request.form.get("notes")
        estat = "actiu"

        # Inserció real a Supabase
        result = supabase.table("persons").insert({
            "nom": nom,
            "cognoms": cognoms,
            "edat": int(edat),
            "tipus": tipus,
            "malalties": malalties,
            "notes": notes,
            "estat": estat
        }).execute()

        new_id = result.data[0]["id"]

        return redirect(f"/p/{new_id}")

    return render_template("register.html")

@app.route("/scan")
def scan():
    return render_template("scan.html")

@app.route("/p/<id>")
def detail(id):
    # Registrar escaneig
    supabase.table("scans_log").insert({
        "person_id": id,
        "agent_id": None
    }).execute()

    # Llegir persona
    result = supabase.table("persons").select("*").eq("id", id).single().execute()

    if result.data is None:
        return "Persona no trobada", 404

    return render_template("detail.html", person=result.data)

if __name__ == "__main__":
    app.run(debug=True)
