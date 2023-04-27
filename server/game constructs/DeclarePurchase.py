'''
A declared purchase that will be put onto the Stack before resolving
'''

class DeclaredPurchase:
    def __init__(self, treasure):
        self.treasure = treasure
        self.name = "Declared Purchase"
        print("Purchase added to stack")

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
        print(f"Player {user.getNumber()} purchased {self.treasure.getName()}!\n")\
        # SYSTEM JSON
        # PLAYER-BOARD JSON for player who bought item
        return

class DeclaredPurchaseMystery:
    def __init__(self, treasure):
        self.treasure = treasure
        self.name = "Declared Purchase Mystery"
        print("Mystery purchase added to stack")

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
        print(f"Player {user.getNumber()} purchased {self.treasure.getName()} (face down)!\n")
        # SYSTEM JSON
        # PLAYER-BOARD JSON for player who bought item
        return
