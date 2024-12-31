from flask import Flask, request, jsonify, render_template
import pandas as pd
from eth_utils import is_checksum_address, to_checksum_address, is_address

app = Flask(__name__)

# Function to validate and convert address to checksum format
def validate_and_format_address(wallet_address):
    # First, check if the address is valid
    if not is_address(wallet_address):
        return None
    
    # If the address is valid but not in checksum format, convert it to checksum format
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

    # Load the spreadsheet (update filepath as needed)
    try:
        df = pd.read_excel("Copy of Resolv Leaderboard.xlsx")  # Replace with your actual file path
    except Exception as e:
        return jsonify({"error": f"Failed to load spreadsheet: {str(e)}"}), 500

    # Focus only on Address (Column C), Rank (Column A), and Points (Column D)
    filtered_df = df[["Rank", "Address", "Points"]]

    # Search for the wallet address in the spreadsheet (case insensitive comparison)
    row = filtered_df.loc[filtered_df["Address"].str.lower() == corrected_address.lower()]

    if row.empty:
        return jsonify({"error": "Wallet address not found"}), 404

    # Return the rank and points in a retro-styled format
    rank = row.iloc[0]["Rank"]
    points = row.iloc[0]["Points"]
    return render_template("points.html", address=corrected_address, rank=rank, points=points)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
