#!/usr/bin/env python

import os
import bb100

def main():
    my_soup = bb100.get_soup(f"https://www.billboard.com/charts/hot-100/{bb100.date}")
    my_playlist = bb100.parse_soup(my_soup)
    my_token = bb100.authenticate()
    bb100.create_playlist(my_token, my_playlist)
    input("Press Enter to Close Application...")


main()


