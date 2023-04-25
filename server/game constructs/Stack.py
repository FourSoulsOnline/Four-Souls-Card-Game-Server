# Contributions
#   Jackson Cashman:
#       All files
#   Ethan Sandoval:
#       __init__, findDice
'''
Stack is an attribute of Room
Dice, Treasure, Loot, Attack Declarations, and Declarations to buy Treasure go in TheStack
Anything that can go in TheStack MUST have a use() function
'''
from Dice import Dice
from DeclareAttack import DeclaredAttack

# TODO: i dont think that players are given an opportunity to react to a card further down the stack
#       after the card above it resolves

class TheStack:
    def __init__(self):
        self.stack = []
        # this holds the thing that was just popped from the stack
        self.lastResolved = 0

    # getters

    def getStackElements(self):
        length = len(self.stack)
        for i in range(length):
            print(self.stack[length - (i + 1)][0].getName())
        return

    def getStack(self):
        return self.stack

    def getLastResolved(self):
        return self.lastResolved
    
    def getJsonObject(self):
        stackObject = {
            "stack": self.stack,
            "lastResolved": self.lastResolved
        }
        return stackObject

    def setLastResolved(self, lis):
        self.lastResolved = lis
        return

    # other functions

    # add something to the end of TheStack
    # obj is a list of (the thing actually being played onto the stack, the player who played that object)
    def add(self, obj):
        self.stack.append(obj)
        return

    # remove the latest element of TheStack
    #def pop(self):
    #    self.stack.pop(-1)
    #    return

    # use all elements of the stack (only for testing)
    def useStack(self):
        while len(self.stack) > 0:
            self.stack[-1][0].use(self.stack[-1][1])
            self.stack.pop(-1)
        return

    # use the latest element of the stack
    def useTop(self):
        # check to make sure the stack isn't empty when trying to use it
        if len(self.stack) <= 0:
            raise IndexError("Cannot use stack when it is empty")
        # if there is a Declared Attack want the stack to not pop until attack is over
        if isinstance(self.stack[-1][0], DeclaredAttack):
            self.stack[-1][0].use(self.stack[-1][1])
            try:
                self.lastResolved = self.stack.pop(-1)
            except:
                return
        # pop the card from the stack then use it, in last resolved 0 is card object, 1 is player object
        else:
            try:
                self.lastResolved = self.stack.pop(-1)
            except:
                return
            self.lastResolved[0].use(self.lastResolved[1])
        return

    '''
    Here lies the first version of use stack
    # use the latest element of the stack
    def useTop(self):
        if len(self.stack) <= 0:
            raise IndexError("Cannot use stack when it is empty")
        self.stack[-1][0].use(self.stack[-1][1])
        try:
            self.lastResolved = self.stack.pop(-1)
        except:
            return
        return
    '''

    # return the most recently played Dice in TheStack
    def findDice(self):
        length = len(self.stack)
        for i in range(len(self.stack)):
            if isinstance(self.stack[length - i - 1][0], Dice) == True:
                return self.stack[(length - i - 1)][0]
        return -1   # -1 would be not found
        # TODO: might raise an error?^

