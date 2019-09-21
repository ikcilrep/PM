from secrets import randbelow
from itertools import chain
from string import ascii_letters, whitespace, punctuation, digits 

# Generates random password with desired length.
def generate_password(length, should_have_whitespaces, should_have_punctuation, should_have_digits):
    characters = ascii_letters
    if should_have_whitespaces:
        characters += whitespace
    if should_have_punctuation:
        characters += punctuation
    if should_have_digits:
        characters += digits
    return ''.join(characters[randbelow(len(characters))] for _ in range(length))
