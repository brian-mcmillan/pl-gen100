import time
import sys
import os
import html_data
from bs4 import BeautifulSoup
from pydoc import html
import requests
import spotipy
import spotipy.util as util

username = input("ENTER USERNAME : ")
date = input("ENTER DATE (YYYY-MM-DD) : ")
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]


def get_soup(url: str) -> html:
    """Get HTML html_data.py"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

    except requests.exceptions.RequestException as error:
        print(f"Failed to connect.")
        raise SystemExit(error)

    return soup


def parse_soup(soup) -> dict:
    """Parse HTML html_data.py, return playlist"""

    # get #1 song/artist
    top_song = soup.findAll("a", {"class": "c-title__link lrv-a-unstyle-link"})[0]
    top_artist = soup.findAll("p", {"class": "c-tagline a-font-primary-l a-font-primary-m@mobile-max lrv-u-color-black "
                                             "u-color-white@mobile-max lrv-u-margin-tb-00 lrv-u-padding-t-025 "
                                             "lrv-u-margin-r-150"})[0]

    # initialize song/artist #2-100 as list
    song = soup.findAll("h3",
                        {"class": "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size"
                                  "-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max "
                                  "a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only",
                         "id": "title-of-a-story"})

    artist = soup.findAll("span",
                          {"class": "c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max"
                                    " u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block"
                                    " a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only",
                           })

    playlist = {top_song.get_text(strip=True): top_artist.get_text(strip=True)}
    for i in range(99):
        playlist[song[i].get_text(strip=True)] = artist[i].get_text(strip=True)

    return playlist


def authenticate():
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


def create_playlist(auth, playlist):
    """Initialize playlist on spotify account"""

    spotify = spotipy.Spotify(auth)
    user = spotify.current_user()

    print(f"Welcome, {user['display_name']}!")
    pl = spotify.user_playlist_create(user=user['id'],
                                      name=f"{date}",
                                      description=f"The top 100 songs from {date}.")
    print(f"Creating Playlist for the top 100 tracks on {date}"), time.sleep(3)

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