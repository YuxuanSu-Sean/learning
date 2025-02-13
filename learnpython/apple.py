from cmd import PROMPT
from unicodedata import name

promot = "hello"

while True:
    name = input(promot)

    if name == "quit!":
        break
    else:
        print("The name " + name.title() + " you called was wrong！！!")


