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

def get_currently_playing(sp): # Retrieve the currently playing track for the authenticated user
    return sp.current_user_playing_track()
