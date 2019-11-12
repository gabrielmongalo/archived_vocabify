import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# Get the user name from terminal
username = sys.argv[1]

# userid = 1234983255

# Erase cache and prompt user permission
try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

# Create Spotify Object

spotifyObject = spotipy.Spotify(auth=token)
