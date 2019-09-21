from secrets import randbelow
from itertools import chain
import string
def generate_password(length, should_have_whitespaces=False, should_have_punctuation=False, should_have_digits=True):
    password = ""
    for _ in range(length):
        password += generate_char(should_have_whitespaces, should_have_punctuation, should_have_digits)
    return password
def generate_char(should_have_whitespaces, should_have_punctuation, should_have_digits):
    characters = string.ascii_letters
    if should_have_whitespaces:
        characters += string.whitespace
    if should_have_punctuation:
        characters += string.punctuation
    if should_have_digits:
        characters += string.digits
    return characters[randbelow(len(characters))]
for x in range(100):
    print(generate_password(x, False, True, True))

