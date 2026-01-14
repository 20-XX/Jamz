import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_SCOPES

def get_spotify_client():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
        scope=SPOTIFY_SCOPES,
        cache_path=".cache"
        )
    )

def get_currently_playing(sp):
    return sp.current_user_playing_track()
