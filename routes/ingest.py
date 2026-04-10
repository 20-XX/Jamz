from flask import Blueprint, jsonify, current_app
import spotipy
from services.spotify import get_currently_playing
from services.ingestion import ingest_current_track
from services.user_service import get_or_create_user

ingest_bp = Blueprint("ingest", __name__)

@ingest_bp.route("/ingest", methods=["POST"])
def ingest():
    try:
        auth_manager = current_app.config["AUTH_MANAGER"]

        # --- AUTH CHECK ---
        if not auth_manager.validate_token(auth_manager.get_cached_token()):
            return jsonify({"error": "User not authenticated"}), 401
        
        sp = spotipy.Spotify(auth_manager=auth_manager)
        # --- GET USER ---
        profile = sp.current_user()
        user_id = get_or_create_user(
            spotify_user_id=profile["id"],
            display_name=profile.get("display_name"))
        
        # --- GET TRACK ---
        data = get_currently_playing(auth_manager)

        if not data:
            return jsonify({"message": "No track currently playing"}), 200

        track_data = data["track_data"]
        played_at = data["played_at"]
        

        # --- INGEST ---
        ingest_current_track(
            user_id=user_id,  # replace later with real user mapping
            track_data=track_data,
            played_at=played_at
        )

        return jsonify({
            "track": track_data["name"],
            "artist": ", ".join(a["name"] for a in track_data["artists"]),
            "message": "Stored track"
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500