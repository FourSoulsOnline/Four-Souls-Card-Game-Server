'''
Event cards that can be found in the Monster deck
Events dont work correctly if they are on the board before the first players turn starts
(not an issue since the deck should be shuffled in that case anyways)
'''

from Cards import Event
from Dice import rollDice
from Decks import Deck
# from PIL import Image

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
        print("Ambushed by an unseen foe! You must attack twice more this turn.\n")
        self.resolve(activePlayer)
        return

class ChestMoney(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        count = rollDice(activePlayer)
        if count < 3:
            activePlayer.addCoins(1)
            print("You open the CHEST and find a meager 1c.\n")
        elif count < 5:
            activePlayer.addCoins(3)
            print("You open the CHEST and find 3c.\n")
        else:
            activePlayer.addCoins(6)
            print("You open the CHEST and find a handsome 6c.\n")
        self.resolve(activePlayer)
        return

class ChestLoot(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        count = rollDice(activePlayer)
        if count < 3:
            activePlayer.loot(1)
            print("You open the CHEST and find a single loot.\n")
        elif count < 5:
            activePlayer.loot(2)
            print("You open the CHEST and find 2 loot cards.\n")
        else:
            activePlayer.loot(3)
            print("You open the CHEST and find a trio of loot.\n")
        self.resolve(activePlayer)
        return

class DarkChest1(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        count = rollDice(activePlayer)
        if count < 3:
            activePlayer.loot(1)
            print("You open the CHEST and find a single loot.\n")
        elif count < 5:
            activePlayer.addCoins(3)
            print("You open the CHEST and find 3c.\n")
        else:
            activePlayer.takeDamage(2, activePlayer)
            print("You open the CHEST to find two live BOMBS!!! You take 2 damage :(\n")
        self.resolve(activePlayer)
        return

class DarkChest2(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        count = rollDice(activePlayer)
        if count < 3:
            activePlayer.addCoins(1)
            print("You open the CHEST and find a meager 1c.\n")
        elif count < 5:
            activePlayer.loot(2)
            print("You open the CHEST and find 2 loot.\n")
        else:
            activePlayer.takeDamage(2, activePlayer)
            print("You open the CHEST to find two live BOMBS!!! You take 2 damage :(\n")
        self.resolve(activePlayer)
        return

class GoldChestLoot(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        count = rollDice(activePlayer)
        if count < 3:
            activePlayer.gainTreasure(1)
            print("Lucky roll, an item was hidden in the chest!!\n")
        elif count < 5:
            activePlayer.loot(1)
            print("You open the CHEST and find a single loot card.\n")
        else:
            activePlayer.loot(2)
            print("You open the CHEST and find 2 loot cards.\n")
        self.resolve(activePlayer)
        return

class GoldChestMoney(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        count = rollDice(activePlayer)
        if count < 3:
            activePlayer.gainTreasure(1)
            print("Lucky roll, an item was hidden in the chest!!\n")
        elif count < 5:
            activePlayer.addCoins(5)
            print("You open the CHEST and find a respectable 5c.\n")
        else:
            activePlayer.addCoins(7)
            print("You open the CHEST and find a handsome 7c!\n")
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
                    print(f"Player {i+1}'s GREED is their downfall, their coin total dropped to 0!!\n")
        # there are 2+ people with the most coins
        else:
            for i in range(len(richest)):
                print(f"{i+1}: Player {richest[i].getNumber()}")
            choice = int(input(f"Force which player to lose all coins?: "))
            choice -= 1
            chosenPlayer = richest[choice]
            chosenPlayer.setCoins(0)
        self.resolve(activePlayer)
        return

# each player takes 2 damage
class MegaTrollBomb(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        players = activePlayer.getRoom().getPlayers()
        print(f"OH NO! It's a {self.name}!!")
        for i in range(len(players)):
            players[i].takeDamage(2, players[i])
            print(f"Player {players[i].getNumber()} is blown up by {self.name}!!!")
        print("")
        self.resolve(activePlayer)
        return

class SecretRoom(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        count = rollDice(activePlayer)
        if count < 2:
            activePlayer.takeDamage(3, activePlayer)
            print("You uncover a terrible secret (3 damage)!!\n")
        elif count < 4:
            # show hand and discard 2
            print("You wasted 2 cards finding this secret room.\n")
            for i in range(2):
                hand = activePlayer.getHand().printCardListNames()
                print("Choose a loot card to discard:")
                choice = int(input(f"  Choice {i+1}: "))
                choice -= 1
                activePlayer.getBoard().discardLoot(activePlayer, choice)
        elif count < 6:
            activePlayer.addCoins(7)
            print(f"You find 7c hidden inside the {self.name}!\n")
        else:
            activePlayer.gainTreasure(1)
            print(f"You find a secret item hidden inside the {self.name}!\n")
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
        print("You find a secret shop! More items can be purchased and you can attack again.\n")
        self.resolve(activePlayer)
        return

# the active player takes 2 damage
class TrollBombs(Event):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def use(self, activePlayer):
        print(f"OH NO! It's a pair of {self.name}!!")
        activePlayer.takeDamage(2, activePlayer)
        print(f"Player {activePlayer.getNumber()} is blown up by {self.name}!!!\n")
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
        print("The walls are shifting...! More monsters appeared and you can attack again.\n")
        self.resolve(activePlayer)
        return

def createEventCards():
    eventDeck = Deck([])
    ambush = Ambush("AMBUSH!", Image.open("test image.jpg"))
    eventDeck.addCardTop(ambush)
    chest_money = ChestMoney("CHEST (MONEY)", Image.open("test image.jpg"))
    eventDeck.addCardTop(chest_money)
    chest_loot = ChestLoot("CHEST (LOOT)", Image.open("test image.jpg"))
    eventDeck.addCardTop(chest_loot)
    dark_chest_1 = DarkChest1("DARK CHEST (1)", Image.open("test image.jpg"))
    eventDeck.addCardTop(dark_chest_1)
    dark_chest_2 = DarkChest1("DARK CHEST (2)", Image.open("test image.jpg"))
    eventDeck.addCardTop(dark_chest_2)
    gold_chest_loot = GoldChestLoot("GOLD CHEST (LOOT)", Image.open("test image.jpg"))
    eventDeck.addCardTop(gold_chest_loot)
    gold_chest_money = GoldChestLoot("GOLD CHEST (MONEY)", Image.open("test image.jpg"))
    eventDeck.addCardTop(gold_chest_money)
    greed = Greed("GREED!", Image.open("test image.jpg"))
    eventDeck.addCardTop(greed)
    mega_troll_bomb = MegaTrollBomb("MEGA TROLL BOMB!", Image.open("test image.jpg"))
    eventDeck.addCardTop(mega_troll_bomb)
    secret_room = SecretRoom("SECRET ROOM!", Image.open("test image.jpg"))
    eventDeck.addCardTop(secret_room)
    shop_upgrade = ShopUpgrade("SHOP UPGRADE!", Image.open("test image.jpg"))
    eventDeck.addCardTop(shop_upgrade)
    troll_bombs = TrollBombs("TROLL BOMBS", Image.open("test image.jpg"))
    eventDeck.addCardTop(troll_bombs)
    xl_floor = XlFloor("XL FLOOR!", Image.open("test image.jpg"))
    eventDeck.addCardTop(xl_floor)
    return eventDeck
