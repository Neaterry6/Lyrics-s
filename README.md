

### ✅ **README.md (API Documentation)**
```md
# Lyrics & Song Metadata API 🎶🚀

This API **fetches song details** (album, release year, artist info) and **finds verified lyrics sources** (Genius, Musixmatch, AZLyrics) using **MusicBrainz & DuckDuckGo Search**.

---

## 🔥 **How It Works**
✅ **User types:** `lyrics Baby by Joeboy`  
✅ **API extracts:** artist & song name automatically  
✅ **Fetches song metadata:** album, release year, genre, artist info (MusicBrainz)  
✅ **Finds lyrics sources:** Genius, Musixmatch, AZLyrics (DuckDuckGo)  
✅ **Returns results in JSON format**  

---

## 🚀 **Endpoints**
### 1️⃣ Fetch Song Details + Lyrics Sources
**GET** `/lyrics?query=<song> by <artist>`  
✅ Fetches song metadata + links to verified lyrics  

**Example Request**
```sh
curl -X GET "https://your-api-url.com/lyrics?query=lyrics Baby by Joeboy"
```

**Example JSON Response**
```json
{
  "title": "Baby",
  "artist": "Joeboy",
  "album": "Love & Light",
  "release_year": "2019",
  "genre": "Afrobeats",
  "lyrics_sources": [
    "https://genius.com/Joeboy-baby-lyrics",
    "https://www.azlyrics.com/lyrics/joeboy/baby.html",
    "https://www.musixmatch.com/lyrics/Joeboy/Baby"
  ]
}
```

---

## ⚡ **Setup & Deployment**
### 1️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 2️⃣ Run API Locally
```sh
python3 app.py
```

### 3️⃣ Deploy on Render / Railway
```sh
git add .
git commit -m "Deploy Lyrics API"
git push origin main
```

---

## 🎯 **Future Improvements**
- ✅ **Improve lyrics sources filtering**  
- ✅ **Expand song metadata sources**  
- ✅ **Add support for more music platforms (Spotify, Apple Music)**  

Try it out and let me know if you want any tweaks! 🚀🔥  
Your API is **ready to rock the music world!** 🎶🎯😎  
What’s next? 
