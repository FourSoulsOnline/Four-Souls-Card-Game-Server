# Contributors: Jackson Cashman
'''
Simple Dice
Dice go in TheStack
'''
import random
from SilverTreasureCards import DiceEffectTreasure

# the code of rollDice is written in other functions, maybe we should replace them with this function call
def rollDice(user):
    dice = Dice()
    # check for sacred heart
    user.addToStack(dice.roll())
    if len(user.getRoom().getStack().getStack()) == 0:
        return  # prevents error when character kills monster during attack, the stack becomes empty causing index error
    # use any cards played in response to the added dice before the dice resolves
    while user.getRoom().getStack().getStack()[-1][0] != dice:
        user.getRoom().getStack().useTop()
    dice = user.getStack().findDice()  # update dice in case it was tampered with by a responding card
    # take the dice off the stack
    user.getStack().useTop()
    count = dice.getResult()
    # check for on x dice roll
    globalEffects = user.getBoard().getGlobalEffects()
    for i in range(len(globalEffects)):
        if isinstance(globalEffects[i][0], DiceEffectTreasure):
            # if the necessary result was rolled to use the card
            itemUser = globalEffects[i][1]
            if count == globalEffects[i][0].getDiceCheck():
                itemUser.addToStack(globalEffects[i][0])
                itemUser.getRoom().useTopStack(itemUser.getNumber())
    return count

class Dice:
    def __init__(self):
        self.result = 0
        self.name = "DICE"

    # getters

    def getResult(self):
        return self.result

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        diceObject = {
            "name": self.getName(),
            "result": self.getResult()
        }
        return diceObject

    # setters

    def use(self, user):
        return self.result

    def roll(self):
        self.result = random.randint(1, 6)
        # print("Dice result " + str(self.result))
        return self

    # set the result of a die to a number between 0 and 6
    def setResult(self, num):
        if num > 6:
            num = 6
        elif num < 0:
            num = 0
        self.result = num
        return self.result

    def incrementUp(self):
        if self.result <= 5:
            self.result += 1
            return self.result
        else:
            return 6

    def incrementDown(self):
        if self.result >= 1:
            self.result -= 1
            return self.result
        else:
            return 0

