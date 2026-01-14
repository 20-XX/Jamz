import os
from dotenv import load_dotenv 
load_dotenv()

RESPONSE_TYPE = 'code' # OAuth2 response type for authorization code flow
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI") 
if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET or not SPOTIPY_REDIRECT_URI: # check for missing env variables
    raise ValueError("Please set SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI in your environment variables.")

SPOTIFY_SCOPES = 'user-read-currently-playing  user-read-playback-state user-modify-playback-state user-read-recently-played' # Spotify API scopes for required permissions

DATABASE_PATH = "spotify.db" # SQLite database file
