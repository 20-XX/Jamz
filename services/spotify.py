import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_SCOPES

def get_spotify_client(): # Initialize and return a Spotify client with OAuth2 authentication
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
        scope=SPOTIFY_SCOPES,
        cache_path=".cache"
        )
    )

def get_currently_playing(auth_manager):
    sp = spotipy.Spotify(auth_manager=auth_manager)

    current = sp.current_user_playing_track()

    if not current or not current.get("item"):
        return None

    return {
        "track_data": current["item"],
        "played_at": current.get("timestamp")  # fallback if needed
    }