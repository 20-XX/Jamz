from db.database import get_db_connection
from datetime import datetime, timedelta

def get_top_artists(spotify_user_id, limit=10):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.name, COUNT(*) as play_count
        FROM play_history p
        JOIN users u ON p.user_id = u.id
        JOIN songs s ON p.song_id = s.id
        JOIN song_artists sa ON s.id = sa.song_id
        JOIN artists a ON sa.artist_id = a.id
        WHERE u.spotify_user_id = ?
        GROUP BY a.id
        ORDER BY play_count DESC
        LIMIT ?
    """, (spotify_user_id, limit))

    results = cursor.fetchall()
    conn.close()

    return results

def get_listening_time(spotify_user_id, days=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT SUM(s.duration_ms) as total_duration
        FROM play_history p
        JOIN users u ON p.user_id = u.id
        JOIN songs s ON p.song_id = s.id
        WHERE u.spotify_user_id = ?
    """

    params = [spotify_user_id]

    if days:
        start_date = (datetime.utcnow() - timedelta(days=days))
        query += " AND p.played_at >= ?"
        params.append(start_date.isoformat())

    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()

    return result["total_duration"] if result["total_duration"] is not None else 0