import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

NOTJUSTOK_SEARCH_URL = "https://notjustok.com/search/"

def search_notjustok(song, artist):
    """Search NotJustOk for the lyrics page link."""
    try:
        search_query = f"{artist} {song} lyrics"
        response = requests.get(NOTJUSTOK_SEARCH_URL + search_query.replace(" ", "-"))
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        first_result = soup.find("a", class_="search-result-link")
        
        if first_result:
            return first_result["href"]
        return None
    except Exception as e:
        print("Error:", str(e))
        return None

def scrape_lyrics(url):
    """Extract lyrics from a NotJustOk lyrics page."""
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        lyrics_section = soup.find("div", class_="lyrics-content")
        
        if lyrics_section:
            return "\n".join([p.text for p in lyrics_section.find_all("p")])
        return None
    except Exception as e:
        print("Error:", str(e))
        return None

@app.route("/lyrics", methods=["GET"])
def get_lyrics():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Provide song name like 'Baby by Joeboy'"}), 400

    artist, song = query.split(" by ") if " by " in query else (None, None)
    if not artist or not song:
        return jsonify({"error": "Invalid format! Example: Baby by Joeboy"}), 400

    lyrics_page = search_notjustok(song, artist)
    
    if lyrics_page:
        lyrics = scrape_lyrics(lyrics_page)
        if lyrics:
            return jsonify({"title": song, "artist": artist, "lyrics": lyrics})
    
    return jsonify({"error": "Lyrics not found!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
