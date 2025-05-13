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

def scrape_lyrics_data(url):
    """Extract lyrics, song image, and artist details from a NotJustOk lyrics page."""
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # ✅ Extract full lyrics
        lyrics_section = soup.find("div", class_="lyrics-content")
        lyrics = "\n".join([p.text for p in lyrics_section.find_all("p")]) if lyrics_section else "Lyrics not found."

        # ✅ Extract song image
        image_section = soup.find("img", class_="featured-image")
        song_image = image_section["src"] if image_section else "No image available."

        # ✅ Extract artist name
        artist_section = soup.find("h2", class_="artist-name")
        artist_name = artist_section.text.strip() if artist_section else "Unknown artist."

        return {"lyrics": lyrics, "image": song_image, "artist": artist_name}
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
        lyrics_data = scrape_lyrics_data(lyrics_page)
        if lyrics_data:
            return jsonify({
                "title": song,
                "artist": lyrics_data["artist"],
                "image": lyrics_data["image"],
                "lyrics": lyrics_data["lyrics"]
            })
    
    return jsonify({"error": "Lyrics not found!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
