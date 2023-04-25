import sys
import json
import ast # abstract syntax tree
from Dice import Dice
from Player import Player
from Characters import createCharacterCards
myDice = Dice()
myDice.roll()
output = myDice.getJsonObject()

print(createCharacterCards())

print(json.dumps(output))

sys.stdout.flush()