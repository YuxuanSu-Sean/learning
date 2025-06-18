from random import randint

class Die():
    def __init__(self, sides):
        self.sides = sides

    def roll_die(self):
        x = randint(1, self.sides)
        print(x)


dice = Die(20)
i = 1
while i <= 10:
    dice.roll_die()
    i += 1