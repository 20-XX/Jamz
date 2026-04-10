import sqlite3
from config import DATABASE_PATH

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row

    # Enforce foreign keys (CRITICAL)
    conn.execute("PRAGMA foreign_keys = ON;")
    
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        spotify_user_id TEXT UNIQUE NOT NULL,
        display_name TEXT
    )
    """)

    # ARTISTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        spotify_artist_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL
    )
    """)

    # SONGS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        spotify_track_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        duration_ms INTEGER,
        album_name TEXT
    )
    """)

    # SONG ↔ ARTIST (MANY-TO-MANY)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS song_artists (
        song_id INTEGER NOT NULL,
        artist_id INTEGER NOT NULL,
        PRIMARY KEY (song_id, artist_id),
        FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE,
        FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE
    )
    """)

    # PLAY HISTORY
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS play_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        song_id INTEGER NOT NULL,
        played_at TIMESTAMP NOT NULL,

        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE,

        UNIQUE(user_id, song_id, played_at)
    )
    """)

    # INDEXES
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_play_user ON play_history(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_play_song ON play_history(song_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_play_time ON play_history(played_at)")

    conn.commit()
    conn.close()