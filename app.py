import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

DUCKDUCKGO_SEARCH_URL = "https://html.duckduckgo.com/html/?q="

def search_duckduckgo(query):
    """Search DuckDuckGo and extract top lyrics page links."""
    try:
        response = requests.get(DUCKDUCKGO_SEARCH_URL + query.replace(" ", "+"))
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for link in soup.select(".result__a"):
            url = link["href"]
            if "genius.com" in url or "azlyrics.com" in url or "musixmatch.com" in url:
                results.append(url)

        return results if results else None
    except Exception as e:
        print("Error:", str(e))
        return None

@app.route("/lyrics", methods=["GET"])
def get_lyrics():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Provide song name with artist in 'Baby Girl by Joeboy' format"}), 400

    artist, song = query.split(" by ") if " by " in query else (None, None)
    if not artist or not song:
        return jsonify({"error": "Invalid format! Try: lyrics Baby Girl by Joeboy"}), 400

    lyrics_sources = search_duckduckgo(f"{song} {artist} lyrics")
    
    if lyrics_sources:
        return jsonify({"lyrics_sources": lyrics_sources})
    
    return jsonify({"error": "Lyrics sources not found!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True
