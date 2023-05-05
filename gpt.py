import openai
import sys
import re
import ast

default_description = "The songs should include the most popular songs and artists of all time."
default_length = 10

def access_gpt(api_key):
    try:
        openai.api_key = api_key
        return True
    except KeyError:
        print("Invalid API Key provided.")
        sys.exit(1)

def new_query(length=default_length, description=default_description):

    query = f"Return a Python3 dictionary of {length} songs in the format (song:artist)." \
            f"{description}"
    try:
        response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant who is knowledgeable about music."},
                        { "role": "user", "content": {query}}
                    ]
        )
        message = response['choices'][0]['message']['content']
        return message
    except openai.error.RateLimitError:
        print("You have exceeded OpenAI credit limit.")
        sys.exit(1)


def parse_message(message):
    message = message.strip("{ ", "{")
    message = message.strip("\n", "")
    message = re.sub(' +', ' ', message)
    playlist = ast.literal_eval(re.search('({.+})', message).group(0))

    return playlist
