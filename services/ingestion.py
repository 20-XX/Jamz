from db.database import get_db_connection
from datetime import datetime

def ingest_current_track(user_id, track_data, played_at):
    conn = get_db_connection()
    cursor = conn.cursor()

    # --- TIMESTAMP ---
    if isinstance(played_at, int):
    # Convert milliseconds → seconds → datetime
        played_at = datetime.utcfromtimestamp(played_at / 1000)

    elif isinstance(played_at, str):
    # Handle ISO string
        played_at = datetime.fromisoformat(played_at.replace("Z", "+00:00"))

    # Final format for SQLite
    played_at = played_at.strftime("%Y-%m-%d %H:%M:%S")
    # --- SONG ---
    cursor.execute("""
        INSERT OR IGNORE INTO songs (spotify_track_id, name, duration_ms, album_name)
        VALUES (?, ?, ?, ?)
    """, (
        track_data["id"],
        track_data["name"],
        track_data["duration_ms"],
        track_data["album"]["name"]
    ))

    cursor.execute(
        "SELECT id FROM songs WHERE spotify_track_id = ?",
        (track_data["id"],)
    )
    song_id = cursor.fetchone()["id"]

    # --- ARTISTS ---
    for artist in track_data["artists"]:
        cursor.execute("""
            INSERT OR IGNORE INTO artists (spotify_artist_id, name)
            VALUES (?, ?)
        """, (artist["id"], artist["name"]))

        cursor.execute(
            "SELECT id FROM artists WHERE spotify_artist_id = ?",
            (artist["id"],)
        )
        artist_id = cursor.fetchone()["id"]

        cursor.execute("""
            INSERT OR IGNORE INTO song_artists (song_id, artist_id)
            VALUES (?, ?)
        """, (song_id, artist_id))

    # --- PLAY HISTORY ---
    cursor.execute("""
        INSERT OR IGNORE INTO play_history (user_id, song_id, played_at)
        VALUES (?, ?, ?)
    """, (user_id, song_id, played_at))
    

    conn.commit()
    conn.close()