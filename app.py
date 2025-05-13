import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ✅ Trusted Lyrics API Sources
GENIUS_SEARCH_URL = "https://genius.com/api/search?q="
MUSIXMATCH_SEARCH_URL = "https://www.musixmatch.com/search/"
AZLYRICS_SEARCH_URL = "https://search.azlyrics.com/search.php?q="

def fetch_lyrics_links(song, artist):
    """Directly search trusted lyrics sources (Genius, Musixmatch, AZLyrics)"""
    try:
        sources = {
            "Genius": f"{GENIUS_SEARCH_URL}{song}+{artist}",
            "Musixmatch": f"{MUSIXMATCH_SEARCH_URL}{song}+{artist}",
            "AZLyrics": f"{AZLYRICS_SEARCH_URL}{song}+{artist}"
        }
        return sources
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

    lyrics_sources = fetch_lyrics_links(song, artist)

    if lyrics_sources:
        return jsonify({"title": song, "artist": artist, "lyrics_sources": lyrics_sources})

    return jsonify({"error": "Lyrics sources not found!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
