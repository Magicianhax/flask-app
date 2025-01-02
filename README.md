Resolv Leaderboard

A web application to check your wallet rank and points for Resolv Labs and calculate NFT rarity with traits, scores, and ranks. Built using Flask and OpenSea API.

Features
	•	Points Leaderboard: Search your wallet address to check your rank and points on the Resolv Leaderboard.
	•	NFT Rarity Checker: Input your NFT Token ID to see detailed traits, rarity scores, and ranks.
	•	Sleek User Interface: A modern and responsive UI for a seamless user experience.
	•	Dynamic Trait Analysis: Displays NFT metadata in a professional table format with rank and OpenSea links.

Live Demo

Try it out: https://resolv-leaderboard.onrender.com/

Homepage (Points Checker)

NFT Rarity Checker

How to Use

Points Leaderboard
	1.	Enter your wallet address on the homepage.
	2.	Click “Check Points”.
	3.	View your rank and points.

NFT Rarity Checker
	1.	Click “Check NFT Rarity” on the homepage.
	2.	Enter the NFT Token ID.
	3.	Click “Check Rarity”.
	4.	View the traits, rarity scores, and rank of your NFT.

Built With
	•	Flask - A lightweight WSGI web application framework.
	•	OpenSea API - For fetching NFT metadata and rarity data.
	•	HTML/CSS - For a sleek and responsive UI design.
	•	SheetDB API - For fetching wallet points and rank data.

Installation
	1.	Clone the repository:

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name


	2.	Create a virtual environment and activate it:

python3 -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`


	3.	Install the required dependencies:

pip install -r requirements.txt


	4.	Run the Flask app:

python app.py


	5.	Open the app in your browser:

http://127.0.0.1:5000



Environment Variables
	•	OpenSea API Key: Add your OpenSea API key in the OPENSEA_API_KEY variable in app.py.

File Structure

/static
    styles.css      # CSS for styling
/templates
    index.html      # Homepage (Points Leaderboard)
    nft_rarity.html # NFT Rarity Checker
    points.html     # Points results page
app.py              # Main Flask app
requirements.txt    # Python dependencies

Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request with improvements or bug fixes.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
	•	Resolv Labs for the inspiration.
	•	OpenSea API for providing access to NFT metadata.
