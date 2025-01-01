from flask import Flask, request, render_template, jsonify
import requests  # Ensure requests is imported for API calls

app = Flask(__name__)

# SheetDB API endpoint
SHEETDB_URL = "https://sheetdb.io/api/v1/cvb0bvbfw7k2z"

# Helper function for validating and formatting wallet addresses
def validate_and_format_address(wallet_address):
    # Placeholder: Replace with actual validation if needed
    return wallet_address  # Assume valid for now

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    wallet_address = request.form.get("walletAddress")

    if not wallet_address:
        return render_template(
            "points.html",
            error="Wallet address is required.",
            link=None
        )

    # Validate and convert the address if needed
    corrected_address = validate_and_format_address(wallet_address)

    if not corrected_address:
        return render_template(
            "points.html",
            error="Invalid wallet address format.",
            link=None
        )

    # Fetch data from SheetDB
    try:
        response = requests.get(SHEETDB_URL)
        if response.status_code != 200:
            return render_template(
                "points.html",
                error=f"Failed to fetch data from SheetDB: {response.status_code}",
                link=None
            )

        # Parse the JSON response
        data = response.json()

        # Search for the wallet address in the data
        matching_row = next((row for row in data if row["Address"].lower() == corrected_address.lower()), None)

        if not matching_row:
            # If no address found, display a custom message and link
            return render_template(
                "points.html",
                error="No address found.",
                link="https://app.resolv.xyz/ref/magician"
            )

        # Extract rank and points from the matching row
        rank = matching_row.get("Rank", "N/A")
        points = matching_row.get("Points", "N/A")

        # Render the points.html template with the address details
        return render_template(
            "points.html",
            address=corrected_address,
            rank=rank,
            points=points,
            error=None,
            link=None
        )

    except Exception as e:
        return render_template(
            "points.html",
            error=f"An error occurred: {str(e)}",
            link=None
        )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
