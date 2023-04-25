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

    # TODO
    def use(self, user):
        # decrement the number of purchases user can initiate this turn
        user.getCharacter().subtractPurchases()
        # remove 10 coins from the player and give them the treasure
        user.subtractCoins(10)
        index = user.getBoard().findMatchingTreasure(self.treasure.getName())
        slotNum = index + 1
        user.purchase(slotNum)
        print(f"Player {user.getNumber()} purchased {self.treasure.getName()}!\n")
        return
