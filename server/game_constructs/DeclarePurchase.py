'''
A declared purchase that will be put onto the Stack before resolving
'''
from JsonOutputHelper import JsonOutputHelper
Json = JsonOutputHelper()

class DeclaredPurchase:
    def __init__(self, treasure):
        self.treasure = treasure
        self.name = "Declared Purchase"
        message = "Purchase added to stack"
        Json.systemOutput(message)

    def getName(self):
        return self.name
    
    def getTreasure(self):
        return self.treasure

    def use(self, user):
        # decrement the number of purchases user can initiate this turn
        user.getCharacter().subtractPurchases()
        # remove 10 coins from the player and give them the treasure
        user.subtractCoins(10)
        index = user.getBoard().findMatchingTreasure(self.treasure.getName())
        slotNum = index + 1
        user.purchase(slotNum)
        message = f"Player {user.getNumber()} purchased {self.treasure.getName()}!"
        Json.systemOutput(message)
        Json.playerBoardOutput(user)
        # TREASURE JSON
        return

class DeclaredPurchaseMystery:
    def __init__(self, treasure):
        self.treasure = treasure
        self.name = "Declared Purchase Mystery"
        message = "Mystery purchase added to stack"
        Json.systemOutput(message)

    def getName(self):
        return self.name
    
    def getTreasure(self):
        return self.treasure

    def use(self, user):
        # decrement the number of purchases user can initiate this turn
        user.getCharacter().subtractPurchases()
        # remove 10 coins from the player
        user.subtractCoins(10)
        # give them the treasure
        slotNum = len(user.getBoard().getTreasures()) + 1
        user.purchase(slotNum)
        message = f"Player {user.getNumber()} purchased {self.treasure.getName()} (face down)!"
        Json.systemOutput(message)
        Json.playerBoardOutput(user)
        # TREASURE JSON
        return
