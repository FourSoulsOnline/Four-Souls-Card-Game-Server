# Contributions
#   Jackson Cashman:
#       __init__, getName, use,
#   Ethan Sandoval:
#       __init__, use
'''
Attacks that are declared by the player go onto TheStack
Combat is contained within the use() function of DeclaredAttack
'''
from Cards import *
from Coins import CoinStack


from Coins import CoinStack

from TreasureReward import TreasureReward

class DeclaredAttack:
    def __init__(self, monster):
        self.monster = monster
        self.name = "Declared Attack"
        print("Attack added to stack")

    # getters

    def getName(self):
        return self.name

    def getMonster(self):
        return self.monster

    # other functions

    def use(self, user):
        # decrement the number of attacks user can initiate this turn
        user.getCharacter().subtractAttacksLeft()
        if user.getCharacter().getMandatoryAttacks() > 1:
            user.getCharacter().subtractMandatoryAttacks()
            # TODO: decrease mandatoryDeckAttacks when attacking the unknown top card

        # loop while user and monster are alive
        while (user.getHp() > 0) and (self.monster.getHp() > 0):
            '''
            # add a new dice to the stack
            attackRoll = Dice()
            user.addToStack(attackRoll.roll())

            # use any cards played in response to the added dice before the dice resolves
            if len(user.getRoom().getStack().getStack()) > 1:
                while user.getRoom().getStack().getStack()[-2][0].getName() != "Declared Attack":
                    user.getRoom().getStack().useTop()
            '''
            from Dice import rollDice
            count = rollDice(user)

            if len(user.getRoom().getStack().getStack()) > 0:
                #if isinstance(user.getRoom().getStack().getStack()[-1][0], Dice):
                    # if user gets successful attack roll
                        #if user.getRoom().getStack().getStack()[-1][0].getResult() >= self.monster.getDiceValue():'''
                if count >= self.monster.getDiceValue():
                    # deal damage to monster
                    user.dealDamage(user.getCharacter().getAttack(), self.monster)
                    #self.monster.takeDamage(user.getCharacter().getAttack(), user)
                    print(f'\n{user.getCharacter().getName()} dealt {user.getCharacter().getAttack()} damage to {self.monster.getName()}\n {user.getCharacter().getName()} HP: {user.getHp()}\n '
                          f'{self.monster.getName()} HP: {self.monster.getHp()}\n')

                    # i think this is uneccessary bc die is proc'd in take damage
                    # if the monster died, claim its rewards, discard it, and fill any empty monster slots
                    #if self.monster.getHp() <= 0:
                    #    self.monster.die(user)

                # if user misses their attack roll
                else:
                    # deal damage to user
                    self.monster.dealDamage(self.monster.getAttack(), user)
                    #user.takeDamage(self.monster.getAttack(), self.monster)
                    print(f'Monster dealt {self.monster.getAttack()} damage to player\n {user.getCharacter().getName()} HP: {user.getHp()}\n '
                          f'{self.monster.getName()} HP: {self.monster.getHp()}\n')
                    # TODO: add player death to stack here
                    if user.getHp() <= 0:
                        print(f"{user.getCharacter().getName()} has died!")

            if self.monster.getHp() == 0:
                return # return early before attempting to pop from empty list (dice was already popped in die())
            # Pops the stack to get rid of the dice roll that was just used
            if len(user.getRoom().getStack().getStack()) > 0:
                from Dice import Dice
                if isinstance(user.getRoom().getStack().getStack()[-1][0], Dice):
                    user.getRoom().getStack().pop()
        return
