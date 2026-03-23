import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
CORS(app)

CH_KEY = os.environ.get("COMPANIES_HOUSE_API_KEY")

@app.route("/api/psc")
def psc():
    number = request.args.get("company_number")
    if not number:
        return jsonify({"error": "company_number required"}), 400
    auth = HTTPBasicAuth(CH_KEY, "")
    base = "https://api.company-information.service.gov.uk"
    profile = requests.get(f"{base}/company/{number}", auth=auth).json()
    pscs = requests.get(f"{base}/company/{number}/persons-with-significant-control", auth=auth).json()
    filings = requests.get(f"{base}/company/{number}/filing-history?category=confirmation-statement&items_per_page=5", auth=auth).json()
    return jsonify({"company_profile": profile, "psc_register": pscs, "filing_history": filings})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
