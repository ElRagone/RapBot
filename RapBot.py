#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from LineRanking import get_best_line
import random

GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup", "what's up", "hey", "yo")

GREETING_OPENINGS = ("Yo", "Hey", "Aye")
GREETING_NICKNAME = ("", " homeboy", "bro", )
GREETING_FOLLOWUP = ("", ", what's crackin'?", ", what it do?", ", what it is?")

def respond(user_input):    
    response = check_for_greeting(user_input)
    
    if not response:
        get_best_line(user_input)
    
    return 'Rap Bot: ' + response

def check_for_greeting(parsed_input):
    """If any of the words in the user's input was a greeting, return a greeting response"""
    for word in parsed_input.split():
        if word.lower() in GREETING_KEYWORDS:
            response = random.choice(GREETING_OPENINGS) + \
                       random.choice(GREETING_NICKNAME) + \
                       random.choice(GREETING_FOLLOWUP)
            response += "\nRap Bot: Are you ready for a collab? Hit me up with a line and I'll respond with some fire!"
            return response

def main():
    while True:
        user_input = input()
        print(respond(user_input))

if __name__ == '__main__':
    main()