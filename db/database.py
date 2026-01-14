import sqlite3
from config import DATABASE_PATH

def get_db_connection(): # Establish and return a connection to the SQLite database
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracks (
            track_id TEXT PRIMARY KEY,
            track_name TEXT NOT NULL,
            artist_name TEXT,
            album_name TEXT
               )
           """) # Table to store track information
   
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS listening_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            track_id TEXT NOT NULL,
            played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (track_id) REFERENCES tracks (track_id)
            )
            """) # Table to store listening history
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_played_at ON listening_history (played_at)
            """) # Index to optimize queries on played_at
    conn.commit()
    conn.close()