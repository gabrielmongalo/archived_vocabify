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

user = spotifyObject.current_user()

displayName = user['display_name']
followers = user['followers']['total']

while True:
    print()
    print(">>>>>> Welcome to Vocabify " + displayName + " !")
    print(">>>>>> You have " + str(followers) + " followers.")
    print()
    print("0 -- Search for an artists")
    print("1 -- Exit")
    print()
    choice = input("Your choice: ")

# Search for the artist
    if choice == "0":
        print("")
        searchQuery = input("Ok, what's their name?: ")
        print()

        # Get the search results
        searchResults = spotifyObject.search(searchQuery, 1, 0, 'artist')

        # Artist Details
        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + ' followers')
        print('Genre: ' + artist['genres'][0])
        webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']

        # Album Details
        trackURIs = []
        trackArt = []
        z = 0

        # Extract some album data
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']

        for i in albumResults:
            print("Album " + i['name'])
            albumID = i['id']
            albumArt = i['images'][0]['url']

            # Extract Track Data
            trackResults = spotifyObject.album_tracks(albumID)['items']

            for i in trackResults:
                print(str(z) + ": " + i['name'])
                trackURIs.append(i['uri'])
                trackArt.append(albumArt)
                z += 1
            print()

            # See Album Art
        while True:
            songSelection = input("Enter a song number to see the album art associated with it (x to exit): ")
            if songSelection == "x":
                break
            elif 0 <= int(songSelection) > len(trackArt):
                print(int(songSelection))
                print(len(trackArt))
                print(str(0 <= int(songSelection) < len(trackArt)))
                songSelection = input("The song number you entered does not exist, please choose another song number: ")
                webbrowser.open(trackArt[int(songSelection)])
            else:
                webbrowser.open(trackArt[int(songSelection)])


    # End the program
    if choice == "1":
        break
