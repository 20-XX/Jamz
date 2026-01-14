def extract_track_data(item):
    # Extract relevant track data from the Spotify API response item
    track = item.get('track', {})
    return {
        'track_id': track.get('id'),
        'track_name': track.get('name'),
        'artist_name': ', '.join(artist['name'] for artist in track.get('artists', [])),
        'album_name': track.get('album', {}).get('name')
    }

def insert_track(conn, track):
    conn.execute("""
        INSERT OR IGNORE INTO tracks (track_id, track_name, artist_name, album_name)
        VALUES (?, ?, ?, ?)
    """, (track['track_id'], track['track_name'], track['artist_name'], track['album_name']))

def insert_listening_history(conn, track_id, played_at):
    conn.execute(""" INSERT OR IGNORE into listening_history (track_id, played_at) values (?, ?) """, (track_id, played_at))