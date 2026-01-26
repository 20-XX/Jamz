import code
from flask import Flask, jsonify, request, redirect
from services.spotify_service import get_spotify_client, get_currently_playing
from db.database import init_db, get_db_connection
from db.models import extract_track_data, insert_track, insert_listening_history
from spotify.auth import auth_manager
import spotipy

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def health_check():
        return "Spotify App is running."
    
    @app.route("/login")
    def login():
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)
    
    @app.route("/callback")
    def callback():
        print("CALLBACK HIT")
        print("ARGS:", request.args)
        code = request.args.get("code")
        auth_manager.get_access_token(code)
        return "Authentication successful. You may close this window."

    
    @app.route("/ingest", methods=["POST"])
    def ingest_currently_playing():
        if not auth_manager.validate_token(auth_manager.get_cached_token()):
            return jsonify({"error": "User not authenticated."}), 401
        
        sp = spotipy.Spotify(auth_manager=auth_manager)
        current = sp.current_user_playing_track()
        print("RAW CURRENTLY PLAYING:", current)
        if not current or not current.get("item"):
            return {"message": "No track currently playing"}, 200

        item = current["item"]

        track = item["name"]
        artist = ", ".join(a["name"] for a in item["artists"])

        print("INGEST DEBUG:", track, artist)

        return {
        "track": track,
        "artist": artist,
        "message": "Stored track"
            }, 201
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
