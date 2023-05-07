import openai
import sys
import re
import ast


def new_query(length, description):

    query = f"Return a Python3 dictionary of {length} songs in the format (song:artist)." \
            f" {description}"
    try:
        openai.api_key = input("Enter OpenAI API key: ")
        response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant who is knowledgeable about music."},
                        {"role": "user", "content": f"{query}"}
                    ]
                )

        message = response['choices'][0]['message']['content']
        return message
    except (openai.error.RateLimitError, openai.error.AuthenticationError) as error:
        print(error)
        sys.exit(1)


def parse_message(message):
    message = message.replace("{ ", "{")
    message = message.replace("\n", "")
    message = re.sub(' +', ' ', message)
    playlist = ast.literal_eval(re.search('({.+})', message).group(0))

    return playlist


def display_playlist(playlist: dict):
    print("\nHere is your personalized playlist :\n")
    i = 1
    for key, value, in playlist.items():
        print(f"{i}.", key, "by", value)
        i += 1
    return
