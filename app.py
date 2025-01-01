from flask import Flask, request, jsonify, render_template
import requests
from eth_utils import is_checksum_address, to_checksum_address, is_address

app = Flask(__name__)

# SheetDB API endpoint
SHEETDB_URL = "https://sheetdb.io/api/v1/cvb0bvbfw7k2z"

# Function to validate and convert address to checksum format
def validate_and_format_address(wallet_address):
    if not is_address(wallet_address):
        return None
    if not is_checksum_address(wallet_address):
        wallet_address = to_checksum_address(wallet_address)
    return wallet_address

@app.route("/", methods=["GET"])
def home():
    # Render the HTML form
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    # Get the wallet address from the form
    wallet_address = request.form.get("walletAddress")

    if not wallet_address:
        return jsonify({"error": "Wallet address is required"}), 400

    # Validate and convert the address if needed
    corrected_address = validate_and_format_address(wallet_address)

    if not corrected_address:
        return jsonify({"error": "Invalid wallet address format"}), 400

    # Fetch data from SheetDB
    try:
        response = requests.get(SHEETDB_URL)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch data from SheetDB"}), 500

        # Parse the JSON response
        data = response.json()

        # Search for the wallet address in the data
        matching_row = next((row for row in data if row["Address"].lower() == corrected_address.lower()), None)

        if not matching_row:
            return jsonify({"error": "Wallet address not found"}), 404

        # Extract rank and points from the matching row
        rank = matching_row.get("Rank", "N/A")
        points = matching_row.get("Points", "N/A")

        # Render the points.html template
        return render_template("points.html", address=corrected_address, rank=rank, points=points)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
