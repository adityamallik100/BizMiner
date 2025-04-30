from flask import Flask, render_template, request, redirect, send_file
from scraper.gmaps_scraper import scrape_google_maps
import pandas as pd
import os

app = Flask(__name__)
DATA_FOLDER = "data"

# Ensure data folder exists
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        category = request.form.get("category")
        location = request.form.get("location")

        if not category or not location:
            return "❌ Please enter both category and location!"

        # Scrape data
        leads = scrape_google_maps(category, location)

        # Save to CSV
        if leads:
            df = pd.DataFrame(leads)
            df.to_csv(os.path.join(DATA_FOLDER, "google_maps_leads.csv"), index=False)

        return redirect("/results")

    return render_template("index.html")

@app.route("/results")
def results():
    file_path = os.path.join(DATA_FOLDER, "google_maps_leads.csv")
    if not os.path.exists(file_path):
        return redirect("/")

    df = pd.read_csv(file_path)
    leads = df.to_dict(orient="records")

    return render_template("results.html", leads=leads)

@app.route("/download")
def download():
    return send_file(os.path.join(DATA_FOLDER, "google_maps_leads.csv"), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
