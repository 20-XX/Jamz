import spotipy
from spotify.auth import auth_manager

def get_spotify_client():
    return spotipy.Spotify(auth_manager=auth_manager)
