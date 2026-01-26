from spotipy.oauth2 import SpotifyOAuth
from config import (
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
    SPOTIPY_REDIRECT_URI,
    SPOTIFY_SCOPES,
    SPOTIFY_CACHE_PATH,
)

auth_manager = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SPOTIFY_SCOPES,
    cache_path=SPOTIFY_CACHE_PATH,
    show_dialog=True,  # forces account selection
)
code = auth_manager.get_authorize_url()  # URL to redirect user for authentication