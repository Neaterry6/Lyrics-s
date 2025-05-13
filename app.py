import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

# ✅ Free APIs for Music Metadata & Lyrics Search
MUSICBRAINZ_API = "https://musicbrainz.org/ws/2/recording/?query="
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

def get_song_metadata(song, artist):
    """Fetch song details (album, release year, genre, artist info) using MusicBrainz API."""
    try:
        response = requests.get(MUSICBRAINZ_API + f'"{song}" AND artist:"{artist}"&fmt=json')
        if response.status_code != 200:
            return None

        data = response.json()
        if "recordings" in data and data["recordings"]:
            recording = data["recordings"][0]  # Take first result
            return {
                "title": recording.get("title", song),
                "artist": artist,
                "album": recording.get("releases", [{}])[0].get("title", "Unknown"),
                "release_year": recording.get("first-release-date", "Unknown"),
                "genre": "Unavailable",
            }
        return None
    except Exception as e:
        print("Error:", str(e))
        return None

@app.route("/song", methods=["GET"])
def get_song_info():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Provide song name with artist in 'Baby Girl by Joeboy' format"}), 400

    artist, song = query.split(" by ") if " by " in query else (None, None)
    if not artist or not song:
        return jsonify({"error": "Invalid format! Try: song Baby Girl by Joeboy"}), 400

    song_metadata = get_song_metadata(song, artist)
    lyrics_sources = search_duckduckgo(f"{song} {artist} lyrics")

    if song_metadata and lyrics_sources:
        song_metadata["lyrics_sources"] = lyrics_sources
        return jsonify(song_metadata)

    return jsonify({"error": "Song details or lyrics sources not found!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
