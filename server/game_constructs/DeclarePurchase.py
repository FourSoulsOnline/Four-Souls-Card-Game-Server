"""
A declared purchase that will be put onto the Stack before resolving
"""
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
        # slotNum = len(user.getBoard().getTreasures()) + 1
        # user.purchase(slotNum)

        # add logic for purchase
        treasureCard = self.treasure
        user.getItems().addCardTop(treasureCard)

        from SilverTreasureCards import PlainSilverTreasure
        from Cards import GoldTreasure
        from Board import checkGuppySoul

        checkGuppySoul(treasureCard, user)
        # the treasure has no tag, return
        if isinstance(treasureCard, PlainSilverTreasure):
            pass
        elif isinstance(treasureCard, GoldTreasure):
            pass
        # the treasure must have a tag, add that card to global effects
        else:
            board = user.getBoard()
            board.getGlobalEffects().append([treasureCard, user])

        message = f"Player {user.getNumber()} purchased {self.treasure.getName()} (face down)!"
        Json.systemOutput(message)
        Json.playerBoardOutput(user)
        return
