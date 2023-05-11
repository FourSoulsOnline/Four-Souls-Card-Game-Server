# Contributions
#   Jackson Cashman:
#       __init__, getName, use,
#   Ethan Sandoval:
#       __init__, use
"""
Attacks that are declared by the player go onto TheStack
Combat is contained within the use() function of DeclaredAttack
"""
from Cards import *
from Coins import CoinStack
from Coins import CoinStack
from TreasureReward import TreasureReward
from JsonOutputHelper import JsonOutputHelper

Json = JsonOutputHelper()


class DeclaredAttack:
    def __init__(self, monster):
        self.monster = monster
        self.name = "Declared Attack"
        message = "Attack added to stack"
        Json.systemOutput(message)

    # getters

    def getName(self):
        return self.name

    def getMonster(self):
        return self.monster

    # other functions

    def use(self, user):
        from Events import Event

        if isinstance(self.monster, Event):
            # use it and end combat
            user.getRoom().addToStack([self.monster, user])
            user.getRoom().useTopStack(0)
        else:
            # decrement the number of attacks user can initiate this turn
            user.getCharacter().subtractAttacksLeft()
            if user.getCharacter().getMandatoryAttacks() > 1:
                user.getCharacter().subtractMandatoryAttacks()
                # TODO: decrease mandatoryDeckAttacks when attacking the unknown top card

            # loop while user and monster are alive
            while (user.getHp() > 0) and (self.monster.getHp() > 0):
                from Dice import rollDice

                message = f"Player {user.getNumber()} rolls for combat with {self.monster.getName()}..."
                Json.systemOutput(message)
                count = rollDice(user)

                if len(user.getRoom().getStack().getStack()) > 0:
                    if count >= self.monster.getDiceValue():
                        # deal damage to monster
                        user.dealDamage(user.getCharacter().getAttack(), self.monster)
                        message = f"Player {user.getNumber()} dealt {user.getCharacter().getAttack()} damage to {self.monster.getName()}!"
                        Json.systemOutput(message)
                        # print(f'\n\n {user.getCharacter().getName()} HP: {user.getHp()}\n {self.monster.getName()} HP: {self.monster.getHp()}\n')

                    # if user misses their attack roll
                    else:
                        # deal damage to user
                        self.monster.dealDamage(self.monster.getAttack(), user)
                        message = f"{self.monster.getName()} dealt {self.monster.getAttack()} damage to Player {user.getNumber()}!"
                        Json.systemOutput(message)
                        # print(f'\n {user.getCharacter().getName()} HP: {user.getHp()}\n  {self.monster.getName()} HP: {self.monster.getHp()}\n')
                    Json.playerBoardOutput(user)
                if (self.monster.getHp() == 0) or (user.getHp() == 0):
                    return  # return early before attempting to pop from empty list (dice was already popped in die())
                # Pops the stack to get rid of the dice roll that was just used
                if len(user.getRoom().getStack().getStack()) > 0:
                    from Dice import Dice

                    # not sure if this reference to stack is neccessary since the dice should already be popped(?)
                    if isinstance(user.getRoom().getStack().getStack()[-1][0], Dice):
                        user.getRoom().getStack().pop()
        return
