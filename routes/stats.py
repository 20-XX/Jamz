from flask import Blueprint, jsonify, request
from db.queries import get_top_artists, get_listening_time

stats_bp = Blueprint("stats", __name__)

@stats_bp.route("/stats/top-artists", methods=["GET"])
def top_artists():
    print("HIT /stats/top-artists")
    try:
        spotify_user_id = request.args.get("spotify_user_id")
        limit = request.args.get("limit", 10)

        # --- VALIDATION ---
        if not spotify_user_id:
            return jsonify({"error": "spotify_user_id is required"}), 400

        try:
            limit = int(limit)
        except ValueError:
            return jsonify({"error": "limit must be an integer"}), 400

        # --- QUERY ---
        results = get_top_artists(spotify_user_id, limit)

        # --- FORMAT RESPONSE ---
        response = [
            {
                "artist": row["name"],
                "plays": row["play_count"]
            }
            for row in results
        ]

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@stats_bp.route("/stats/listening-time", methods=["GET"])
def listening_time():
    print("HIT /stats/listening-time")
    try:
        spotify_user_id = request.args.get("spotify_user_id")
        days = request.args.get("days")

        # --- VALIDATION ---
        if not spotify_user_id:
            return jsonify({"error": "spotify_user_id is required"}), 400
        
        if days:
            try:
                days = int(days)
            except ValueError:
                return jsonify({"error": "days must be an integer"}), 400
        # --- QUERY ---
        total_duration_ms = get_listening_time(spotify_user_id, days)

        # --- CONVERSION ---
        total_minutes = total_duration_ms / 60000
        total_hours = total_minutes / 60

        return jsonify({"total_minutes": round(total_minutes, 2), "total_hours": round(total_hours, 2)}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500