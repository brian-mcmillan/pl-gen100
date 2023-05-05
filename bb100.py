from bs4 import BeautifulSoup
from pydoc import html
import requests


def get_soup(url: str) -> html:
    """Get HTML data"""
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
