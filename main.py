#!/usr/bin/env python

import os
import bb100
import gpt
import spotify
import sys

CLIENT_SECRET = os.environ['CLIENT_SECRET']
CLIENT_ID = os.environ['CLIENT_ID']
REDIRECT_URI = os.environ['REDIRECT_URI']

print("Welcome to the Spotify Playlist Generator.")
user = input("Enter Spotify Username: ")
token = spotify.access_spotify(user, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

def main():
    print("Enter '1' to generate a playlist of the top 100 songs for a given date.")
    print("Enter '2' to generate a playlist based on artist, song, sentiment, or genre!")
    print("Enter 'Q' to Quit")
    decision = input()
    if decision == '1':
        decision_1()
    elif decision == '2':
        decision_2()
    elif decision =='Q'.lower():
        sys.exit(0)
    else:
        print("Invalid input.")
        main()

def decision_1():
    date = input("Enter date (YYYY-MM-DD) : ")
    my_soup = bb100.get_soup(f"https://www.billboard.com/charts/hot-100/{date}")
    my_playlist = bb100.parse_soup(my_soup)
    spotify.create_playlist(token, my_playlist, name=date, description=f"The top 100 songs from {date}")

def decision_2():
    api_key = input("Enter OpenAI API Key:")
    authorized = gpt.access_gpt(api_key)
    if authorized:
        description = input("Describe your playlist in one or two sentences.")
        length = input("How many songs would you like to generate?")
        message = gpt.new_query(length, description)
        my_playlist = gpt.parse_message(message)
        print("message")
        name = input("What would you like to name your playlist?: ")
        spotify.create_playlist(token, my_playlist, name=name, description='')

if __name__=="__main__":
    main()



