from flask import Flask, request, render_template
import requests
import time

app = Flask(__name__)

# OpenSea API Key and Collection details
OPENSEA_API_KEY = "137f08e3f45f431e8065e56fa1251c51"
CONTRACT_ADDRESS = "0x2E1E87d0A10dd59C332b1C0e8A894b738dF7059E"
COLLECTION_SLUG = "blueprint-by-resolv"
TOTAL_NFTS = 1253  # Total number of NFTs in the collection

# SheetDB API Endpoint for Wallet Points
SHEETDB_URL = "https://sheetdb.io/api/v1/cvb0bvbfw7k2z"

# Helper function to fetch NFT metadata
def fetch_nft_metadata(contract_address, token_id):
    url = f"https://api.opensea.io/api/v2/chain/arbitrum/contract/{contract_address}/nfts/{token_id}"
    headers = {
        "accept": "application/json",
        "x-api-key": OPENSEA_API_KEY,
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 429:  # Rate limit hit
        time.sleep(60)
        return fetch_nft_metadata(contract_address, token_id)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Helper function to fetch wallet data
def fetch_wallet_data():
    response = requests.get(SHEETDB_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route("/", methods=["GET"])
def home():
    # Render the points-checking homepage
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    wallet_address = request.form.get("walletAddress")

    if not wallet_address:
        return render_template("points.html", error="Wallet address is required.", link=None)

    wallet_data = fetch_wallet_data()
    if not wallet_data:
        return render_template("points.html", error="Failed to fetch wallet data.", link=None)

    matching_row = next((row for row in wallet_data if row["Address"].lower() == wallet_address.lower()), None)
    if not matching_row:
        return render_template(
            "points.html",
            error="No address found.",
            link="https://app.resolv.xyz/ref/magician"
        )

    rank = matching_row.get("Rank", "N/A")
    points = matching_row.get("Points", "N/A")

    return render_template(
        "points.html",
        address=wallet_address,
        rank=rank,
        points=points,
        error=None,
        link=None
    )

@app.route("/nft-rarity", methods=["GET", "POST"])
def nft_rarity():
    if request.method == "POST":
        token_id = request.form.get("tokenId")

        if not token_id:
            return render_template("nft_rarity.html", error="Token ID is required.")

        metadata = fetch_nft_metadata(CONTRACT_ADDRESS, token_id)
        if metadata:
            nft_data = metadata.get("nft", {})
            traits = nft_data.get("traits", [])
            rarity_scores = {}
            total_rarity_score = 0

            if traits:
                for trait in traits:
                    trait_type = trait["trait_type"]
                    value = trait["value"]
                    count = 10  # Mocked count for testing; replace with actual data
                    rarity_score = TOTAL_NFTS / count
                    rarity_scores[f"{trait_type}: {value}"] = rarity_score
                    total_rarity_score += rarity_score

            rarity = nft_data.get("rarity", {})
            rank = rarity.get("rank")
            max_rank = rarity.get("max_rank", TOTAL_NFTS)
            rarity_percentage = f"Top {round((rank / max_rank) * 100, 2)}%" if rank and max_rank else None

            return render_template(
                "nft_rarity.html",
                token_id=token_id,
                traits=traits,
                rank=rank,
                max_rank=max_rank,
                rarity_percentage=rarity_percentage,
                rarity_scores=rarity_scores,
                total_rarity_score=total_rarity_score,
                metadata=nft_data,
                error=None,
            )
        else:
            return render_template(
                "nft_rarity.html",
                error="Failed to fetch NFT data. Please ensure the token ID is correct.",
            )

    return render_template("nft_rarity.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
