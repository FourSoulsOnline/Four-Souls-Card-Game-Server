'''
Event cards that can be found in the Monster deck
Events dont work correctly if they are on the board before the first players turn starts
(not an issue since the deck should be shuffled in that case anyways)
'''

from Cards import Event
#from Dice import rollDice
from Decks import Deck
from JsonOutputHelper import JsonOutputHelper
Json = JsonOutputHelper()

# the active player must attack the monster deck 2 times this turn
# TODO: force this to target the unknown top monster
class Ambush(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        activePlayer.getCharacter().addAttacksLeft()
        activePlayer.getCharacter().addAttacksLeft()
        activePlayer.getCharacter().addMandatoryAttacks()
        activePlayer.getCharacter().addMandatoryAttacks()
        message = f"Player {activePlayer.getNumber()} is ambushed by an unseen foe! They must attack twice more this turn."
        Json.systemOutput(message)
        self.resolve(activePlayer)
        return

class ChestMoney(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        message = f"Rolling for {self.name}..."
        Json.systemOutput(message)
        count = rollDice(activePlayer)
        if count < 3:
            message = f"Player {activePlayer.getNumber()} opens {self.name} and finds a meager 1c."
            Json.systemOutput(message)
            activePlayer.addCoins(1)
        elif count < 5:
            message = f"Player {activePlayer.getNumber()} opens {self.name} and finds 3c."
            Json.systemOutput(message)
            activePlayer.addCoins(3)
        else:
            message = f"Player {activePlayer.getNumber()} opens {self.name} and finds a cool 6c."
            Json.systemOutput(message)
            activePlayer.addCoins(6)
        self.resolve(activePlayer)
        return

class ChestLoot(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        message = f"Rolling for {self.name}..."
        Json.systemOutput(message)
        count = rollDice(activePlayer)
        if count < 3:
            message = f"Player {activePlayer.getNumber()} opens {self.name} and finds a single loot."
            Json.systemOutput(message)
            activePlayer.loot(1)
        elif count < 5:
            message = f"Player {activePlayer.getNumber()} opens {self.name} and finds 2 loot cards."
            Json.systemOutput(message)
            activePlayer.loot(2)
        else:
            message = f"Player {activePlayer.getNumber()} opens {self.name} and finds a triplet of loot!"
            Json.systemOutput(message)
            activePlayer.loot(3)
        self.resolve(activePlayer)
        return

class DarkChest1(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        message = f"Rolling for {self.name}..."
        Json.systemOutput(message)
        count = rollDice(activePlayer)
        if count < 3:
            message = f"Player {activePlayer.getNumber()} opens {self.name} and finds a single loot."
            Json.systemOutput(message)
            activePlayer.loot(1)
        elif count < 5:
            message = f"Player {activePlayer.getNumber()} opens {self.name} and finds 3c."
            Json.systemOutput(message)
            activePlayer.addCoins(3)
        else:
            message = f"Player {activePlayer.getNumber()} opens {self.name} and finds a pair of Troll Bombs (-2 HP)!!. D:"
            Json.systemOutput(message)
            activePlayer.takeDamage(2, activePlayer)
        self.resolve(activePlayer)
        return

class DarkChest2(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        message = f"Rolling for {self.name}..."
        Json.systemOutput(message)
        count = rollDice(activePlayer)
        if count < 3:
            message = f"Player {activePlayer.getNumber()} opens {self.name} and finds a meager 1c."
            Json.systemOutput(message)
            activePlayer.addCoins(1)
        elif count < 5:
            message = f"Player {activePlayer.getNumber()} opens {self.name} and finds 2 loot."
            Json.systemOutput(message)
            activePlayer.loot(2)
        else:
            message = f"Player {activePlayer.getNumber()} opens {self.name} and finds a pair of Troll Bombs (-2 HP)!! D:"
            Json.systemOutput(message)
            activePlayer.takeDamage(2, activePlayer)
        self.resolve(activePlayer)
        return

class GoldChestLoot(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        message = f"Rolling for {self.name}..."
        Json.systemOutput(message)
        count = rollDice(activePlayer)
        if count < 3:
            message = f"Player {activePlayer.getNumber()} got a lucky roll, an item was hidden in {self.name}!! :D"
            Json.systemOutput(message)
            activePlayer.gainTreasure(1)
        elif count < 5:
            message = f""
            Json.systemOutput(message)
            activePlayer.loot(1)
        else:
            message = f"Player {activePlayer.getNumber()} opens {self.name} and finds a pair of loot cards."
            Json.systemOutput(message)
            activePlayer.loot(2)
        self.resolve(activePlayer)
        return

class GoldChestMoney(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        message = f"Rolling for {self.name}..."
        Json.systemOutput(message)
        count = rollDice(activePlayer)
        if count < 3:
            message = f"Player {activePlayer.getNumber()} got a lucky roll, an item was hidden in {self.name}!! :D"
            Json.systemOutput(message)
            activePlayer.gainTreasure(1)
        elif count < 5:
            message = f"Player {activePlayer.getNumber()} opens {self.name} and finds a respectable 5c. :)"
            Json.systemOutput(message)
            activePlayer.addCoins(5)
        else:
            message = f"Player {activePlayer.getNumber()} opens {self.name} and finds a handsome 7c. B)"
            Json.systemOutput(message)
            activePlayer.addCoins(7)
        self.resolve(activePlayer)
        return

# choose a player with the most c or tied for the most. that player loses all their c
class Greed(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        players = activePlayer.getRoom().getPlayers()
        most = 0
        richest = []
        # find the richest player
        for i in range(len(players)):
            # players[i] has the most money so far in the loop
            if players[i].getCoins() > most:
                most = players[i].getCoins()
                # replace the list with just players[i]
                richest = [players[i]]
            # players[i] is tried for the most money so far in the loop
            elif players[i].getCoins() == most:
                # add players[i] to the current list
                richest.append(players[i])
        # do nothing if no one has any coins
        if most == 0:
            pass
        # if there is no tie for richest
        elif len(richest) == 1:
            for i in range(len(players)):
                if richest[0] == players[i]:
                    players[i].setCoins(0)
                    message = f"Player {i+1}'s GREED is their downfall, their coin total dropped to 0!! >:)"
                    Json.systemOutput(message)
        # there are 2+ people with the most coins
        else:
            playerOption = []
            # create an array of strings to pass into JSON
            for i in richest:
                playerOption.append(i.getName())
            # this passes and prints data for JSON
            message = f"Force which player to lose all coins?"
            Json.choiceOutput(activePlayer.getSocketId(), message, playerOption)
            # then look for input from button press
            playerChoice = int(input())
            chosenPlayer = richest[playerChoice-1]
            chosenPlayer.setCoins(0)
        self.resolve(activePlayer)
        return

# each player takes 2 damage
class MegaTrollBomb(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        players = activePlayer.getRoom().getPlayers()
        message = f"OH NO! It's a {self.name}!! D:>"
        Json.systemOutput(message)
        for i in range(len(players)):
            message = f"Player {players[i].getNumber()} is blown up by {self.name}!!!"
            Json.systemOutput(message)
            players[i].takeDamage(2, players[i])
        self.resolve(activePlayer)
        return

class SecretRoom(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        message = f"Rolling for {self.name}..."
        Json.systemOutput(message)
        count = rollDice(activePlayer)
        if count < 2:
            message = f"Player {activePlayer.getNumber()} uncovers a terrible secret (3 damage)!! x_x"
            Json.systemOutput(message)
            activePlayer.takeDamage(3, activePlayer)
        elif count < 4:
            message = f"Player {activePlayer.getNumber()} wasted 2 loot cards finding this secret room."
            Json.systemOutput(message)
            # show hand and discard 2
            for i in range(2):
                activePlayer.chooseDiscard(0, activePlayer)
        elif count < 6:
            message = f"Player {activePlayer.getNumber()} finds a convenient 7c hidden inside the secret room!"
            Json.systemOutput(message)
            activePlayer.addCoins(7)
        else:
            message = f"Player {activePlayer.getNumber()} finds a secret item hidden inside the secret room! B)"
            Json.systemOutput(message)
            activePlayer.gainTreasure(1)
        self.resolve(activePlayer)
        return

# expand treasure slots by 2. the active player may attack again this turn
class ShopUpgrade(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, player):
        activePlayer = player.getRoom().getActivePlayer()
        # add two shop slots
        activePlayer.getBoard().addTreasureSlot()
        activePlayer.getBoard().addTreasureSlot()
        # add an attack to the active player
        activePlayer.getCharacter().addAttacksLeft()
        message = f"Player {activePlayer.getNumber()} finds a secret shop! More items can be purchased and they can attack again."
        Json.systemOutput(message)
        self.resolve(activePlayer)
        return

# the active player takes 2 damage
class TrollBombs(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        message = f"OH NO! It's a pair of Troll Bombs!!"
        Json.systemOutput(message)
        message = f"Player {activePlayer.getNumber()} is blown up by {self.name}!!! :("
        Json.systemOutput(message)
        activePlayer.takeDamage(2, activePlayer)
        self.resolve(activePlayer)
        return

# expand monster slots by 1. the active player may attack again this turn
class XlFloor(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, player):
        activePlayer = player.getRoom().getActivePlayer()
        # add monster slot
        activePlayer.getBoard().addMonsterSlot()
        # add an attack to the active player
        activePlayer.getCharacter().addAttacksLeft()
        message = f"The walls are shifting...! More monsters appeared and Player {activePlayer.getNumber()} can attack again."
        Json.systemOutput(message)
        self.resolve(activePlayer)
        return

def createEventCards():
    eventDeck = Deck([])
    ambush = Ambush("Ambush!", "test image.jpg")
    eventDeck.addCardTop(ambush)
    chest_money = ChestMoney("Chest (Coin)", "test image.jpg")
    eventDeck.addCardTop(chest_money)
    chest_loot = ChestLoot("Chest (Loot)", "test image.jpg")
    eventDeck.addCardTop(chest_loot)
    dark_chest_1 = DarkChest1("Dark Chest (Loot 1)", "test image.jpg")
    eventDeck.addCardTop(dark_chest_1)
    dark_chest_2 = DarkChest1("Dark Chest (Gain 1)", "test image.jpg")
    eventDeck.addCardTop(dark_chest_2)
    gold_chest_loot = GoldChestLoot("Gold Chest (Loot)", "test image.jpg")
    eventDeck.addCardTop(gold_chest_loot)
    gold_chest_money = GoldChestLoot("Gold Chest (Gain)", "test image.jpg")
    eventDeck.addCardTop(gold_chest_money)
    greed = Greed("Greed!", "test image.jpg")
    eventDeck.addCardTop(greed)
    mega_troll_bomb = MegaTrollBomb("Mega Troll Bomb!", "test image.jpg")
    eventDeck.addCardTop(mega_troll_bomb)
    secret_room = SecretRoom("Secret Room!", "test image.jpg")
    eventDeck.addCardTop(secret_room)
    shop_upgrade = ShopUpgrade("Shop Upgrade!", "test image.jpg")
    eventDeck.addCardTop(shop_upgrade)
    troll_bombs = TrollBombs("Troll Bombs", "test image.jpg")
    eventDeck.addCardTop(troll_bombs)
    xl_floor = XlFloor("XL Floor!", "test image.jpg")
    eventDeck.addCardTop(xl_floor)
    return eventDeck
