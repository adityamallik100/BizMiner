# BizMiner

BizMiner is a Google Maps web scraper built using Python, Flask, and Selenium. It allows users to extract structured business data such as name, address, phone number, website, and email from Google Maps based on a specified business category and location.

---

## Features

- Scrapes business listings from Google Maps
- Extracts business names, addresses, phone numbers, websites, and emails
- Uses WHOIS lookup to retrieve email addresses when not available on websites
- Responsive Bootstrap-based UI
- Results displayed in a tabular format
- CSV download functionality
- Simple query form to input business category and location
- Optional loading animation while scraping

---
BizMiner/
│
├── app.py                  # Flask entrypoint
├── scraper/
│   └── gmaps_scraper.py    # Google Maps scraping logic
├── templates/
│   ├── index.html          # Search input form
│   └── results.html        # Results display table
├── static/                 # Optional: loading animations, styles
├── data/
│   └── google_maps_leads.csv
├── requirements.txt
├── README.md
└── venv/                   # Virtual environment (not included in repo)


##Future Improvements:##

Improved email validation

Excel export support

Cloud deployment (Render, Railway, Heroku, etc.)

User authentication and history tracking

Support for scraping multiple cities in a single run





Developed by Aditya Mallik. For contributions or inquiries, feel free to open an issue on GitHub.

