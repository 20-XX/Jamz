# app.py

from services.spotify_service import get_spotify_client, get_currently_playing
from db.database import init_db, get_db_connection
from db.models import extract_track_data, insert_track, insert_listening_event

def ingest_current_track():
    sp = get_spotify_client()
    current = get_currently_playing(sp)

    if not current or not current.get("item"):
        return "Nothing playing"

    track = extract_track_data(current["item"])
    played_at = current["timestamp"]

    conn = get_db_connection()
    insert_track(conn, track)
    insert_listening_event(conn, track["track_id"], played_at)
    conn.commit()
    conn.close()

    return f"Stored {track['track_name']}"

if __name__ == "__main__":
    init_db()
    print(ingest_current_track())
