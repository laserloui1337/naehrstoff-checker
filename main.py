from flask import Flask, request, jsonify
import csv
import re

app = Flask(__name__)

# Wirkstoffe aus CSV einlesen
def lade_wirkstoffe():
    try:
        with open("Naehrstoffe.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row["Wirkstoff"].strip().lower() for row in reader if row.get("Wirkstoff")]
    except Exception as e:
        return []

erlaubte_wirkstoffe = lade_wirkstoffe()

@app.route("/check", methods=["POST"])
def check_wirkstoffe():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No input text"}), 400

    kandidaten = set(re.findall(r'\b[A-ZÄÖÜ][a-zäöüßA-ZÄÖÜ]{2,}\b', text))
    kandidaten = {w.lower() for w in kandidaten}
    nicht_erlaubt = [w for w in kandidaten if not any(w in s for s in erlaubte_wirkstoffe)]

    return jsonify({
        "valid": not bool(nicht_erlaubt),
        "not_in_csv": nicht_erlaubt
    })

@app.route("/")
def home():
    return "Nährstoff-Checker läuft."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
