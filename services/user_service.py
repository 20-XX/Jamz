from db.database import get_db_connection

def get_or_create_user(spotify_user_id, display_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert if not exists
    cursor.execute("""
        INSERT OR IGNORE INTO users (spotify_user_id, display_name)
        VALUES (?, ?)
    """, (spotify_user_id, display_name))

    # Fetch user id
    cursor.execute("""
        SELECT id FROM users WHERE spotify_user_id = ?
    """, (spotify_user_id,))

    user = cursor.fetchone()

    conn.commit()
    conn.close()

    if user is None:
        raise Exception("Failed to get or create user")

    return user["id"]