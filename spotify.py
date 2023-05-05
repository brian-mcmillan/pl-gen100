import spotipy
import spotipy.util as util
import time

def access_spotify(username, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI):
    """Authenticate user account credentials"""

    try:
        token = util.prompt_for_user_token(username,
                                           # scope -> what information user is willing to give program
                                           scope='user-library-read playlist-modify-public',
                                           client_id=CLIENT_ID,
                                           client_secret=CLIENT_SECRET,
                                           redirect_uri=REDIRECT_URI)

        if token:
            print("Authorized.")
            return token


    except ConnectionError as error:
        print("Error authorizing spotify account. Check credentials and try again.")
        SystemExit(error)


def create_playlist(auth, playlist, name, description):
    """Initialize playlist on spotify account"""

    spotify = spotipy.Spotify(auth)
    user = spotify.current_user()

    print(f"Welcome, {user['display_name']}!")
    pl = spotify.user_playlist_create(user=user['id'],
                                      name=f"{name}",
                                      description=f"{description}.")
    print(f"Creating Playlist"), \
    time.sleep(3)

    for key, value in playlist.items():
        # EX: key = September, value = Earth Wind and Fire
        # Searches for "Earth Wind and Fire" by type, track. Returns result[0] (most popular)."
        track_info = spotify.search(q=f"track:%@{key}", type="track")
        # add to pl
        print(f"adding track {key} by {value}")
        try:
            spotify.user_playlist_add_tracks(user['id'], pl['id'], [track_info["tracks"]["items"][0]["id"]], position=0)
        except IndexError:
            print(f"failed to locate track {key} by {value}")
            continue

    print("\nPlaylist Successfully Created.")
