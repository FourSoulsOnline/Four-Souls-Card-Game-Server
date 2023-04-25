# Contributions
#   Jackson Cashman:
#       Money, Bomb, DiceShard, MegaBattery, PillsYellow, PillsRed, PillsBlue, TheMagician, TheHighPriestess,
#       TheLovers, TheChariot, Justice, WheelOfFortune, Strength, Death, Temperance, TheDevil, TheTower, TheStars,
#       Judgement, Ehwaz, BlankRune
#   Ethan Sandoval:
#       DiceShard, The Emperor, The Hermit, The Moon, The World, The Hierophant, The Hanged Man, Soul Heart
#   Daniel De Guzman:
#       getJsonObject()

'''
This file contains the classes for each archetype of loot card (such as coin rewarding cards) as well as
the creation of the actual cards in those archetypes
'''
from Coins import CoinStack
from Cards import *
# from PIL import Image
from Decks import Deck
from Dice import *
from Stack import *

# Loot cards that give cents and nothing more
class Money(Loot):
    def __init__(self, name, picture, count):
        super().__init__(name, picture)
        self.count = count

    # getters

    def getName(self):
        return self.name

    def getCount(self):
        return self.count
    
    # Return this object in json structure for GameStates - D.D.
    def getJsonObject(self):
        lootMoneyObject = {
            "card": super().getJsonObject(),
            "count": self.count
        }
        return lootMoneyObject

    # other functions

    def use(self, user):
        user.addCoins(self.count)
        user.subtractTapped()
        return self.count


def createMoneyCards():
    # Here are all loot cards that exclusively give money added to moneyDeck
    moneyDeck = Deck([])
    a_penny = Money("A Penny!", "penny picture.png", 1)
    for i in range(2):
        moneyDeck.addCardTop(a_penny)
    two_cents = Money("2 Cents!", "penny picture.png", 2)
    for i in range(6):
        moneyDeck.addCardTop(two_cents)
    three_cents = Money("3 Cents!", "penny picture.png", 3)
    for i in range(11):
        moneyDeck.addCardTop(three_cents)
    four_cents = Money("4 Cents!", "penny picture.png", 4)
    for i in range(12):
        moneyDeck.addCardTop(four_cents)
    a_nickel = Money("A Nickel!", "penny picture.png", 5)
    for i in range(6):
        moneyDeck.addCardTop(a_nickel)
    a_dime = Money("A Dime!!", "penny picture.png", 10)
    moneyDeck.addCardTop(a_dime)
    return moneyDeck


# Loot cards that deal damage directly to an Entity
class Bomb(Loot):
    def __init__(self, name, picture, damage):
        super().__init__(name, picture)
        self.damage = damage

    def getName(self):
        return self.name
    
    # Return this object in json structure for GameStates - D.D.
    def getJsonObject(self):
        bombLootObject = {
            "card": super().getJsonObject(),
            "damage": self.damage
        }
        return bombLootObject

    def use(self, user):
        room = user.getRoom()
        # display the characters in the room
        playerList = room.getPlayers()
        for i in range(len(playerList)):
            print(f"{1+i}: {playerList[i].getCharacter().getName()}\n  HP: {playerList[i].getCharacter().getHp()}")
        # display the active monsters
        monsterList = user.getBoard().getMonsters()
        for i in range(len(monsterList)):
            print(f"{len(playerList) + i + 1}: {monsterList[i][-1].getName()}\n  HP: {monsterList[i][-1].getHp()}")
        target = input("Target which creature with " + str(self.getName()) + "? :")
        # bomb the selected target
        if int(target) <= len(playerList): # bomb player
            room.getPlayers()[int(target) - 1].takeDamage(self.damage, user)
        else: # bomb monster
            user.getBoard().getMonsters()[int(target) - 1 - len(playerList)][-1].takeDamage(self.damage, user)
        user.subtractTapped()
        return


def createBombCards():
    # Here are all loot cards that are bombs, added to bombDeck
    bombDeck = Deck([])
    bomb = Bomb("Bomb!", "test image.jpg", 1)
    for i in range(5):
        bombDeck.addCardTop(bomb)
    gold_bomb = Bomb("Gold Bomb!!", "test image.jpg", 3)
    bombDeck.addCardTop(gold_bomb)
    return bombDeck


# TODO: "choose a dice roll. its controller rerolls it"
#        the "its controller" part is not implemented,
#        which is relevant for cards with effects like +1 to all dice rolls
#        ...or maybe that is already implemented since the user shouldnt change...?
class DiceShard(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)
    
    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    # dice shard rerolls the most recently played Dice in TheStack
    def use(self, user):
        room = user.getRoom()
        stack = room.getStack()
        dice = stack.findDice()
        if isinstance(dice, Dice) == True:
            dice.roll()
        user.subtractTapped()
        return


def createDiceShardCards():
    diceShardDeck = Deck([])
    dice_shard = DiceShard("Dice Shard", "test image.jpg")
    for i in range(3):
        diceShardDeck.addCardTop(dice_shard)
    return diceShardDeck

# recharge an item
# TODO: putting this off because choosing what item to recharge is complcated and will need to be redone when integrated to website anyways
class LilBattery(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        room = user.getRoom()
        players = room.getPlayers()
        numPlayers = len(players)
        allItems = Deck([])
        # put all items into one deck
        for i in range(numPlayers):
            allItems.combineDeck(players[i].getItems())
        allItems.printCardListNames()
        num = int(input("Recharge which item?: "))
        # TODO
        user.subtractTapped()
        return

class MegaBattery(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        room = user.getRoom()
        players = room.getPlayers()
        allItems = Deck([])
        num = int(input("Which player will you recharge all items?: "))
        num -= 1
        chosenDeck = players[num].getItems()
        for i in range(chosenDeck.getDeckLength()):
            if isinstance(chosenDeck.getCardList()[i], GoldTreasure):
                chosenDeck.getCardList()[i].setTapped(False)
        user.subtractTapped()
        return

def createMegaBatteryCards():
    megaBatteryDeck = Deck([])
    mega_battery = MegaBattery("Mega Battery", "test image.jpg")
    megaBatteryDeck.addCardTop(mega_battery)
    return megaBatteryDeck

class PillsYellow(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        count = rollDice(user)
        if count < 3:
            user.addCoins(4)
            print("+4 coins!\n")
        elif count < 5:
            user.addCoins(7)
            print("Jackpot, +7 coins!\n")
        else:
            user.subtractCoins(4)
            print("Bad trip, -4 coins!\n")
        user.subtractTapped()
        return

class PillsRed(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        count = rollDice(user)
        if count < 3:
            attack = user.getCharacter().getAttack()
            user.getCharacter().setAttack(attack + 1)
            print("Sick, +1 attack!\n")
        elif count < 5:
            hp = user.getCharacter().getHp()
            user.getCharacter().setHp(hp + 1)
            print("Sweet, +1 HP!\n")
        else:
            user.takeDamage(1, user)
            print("Bad trip, -1 HP!\n")
        user.subtractTapped()
        return

class PillsBlue(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        count = rollDice(user)
        if count < 3:
            user.loot(1)
            print("+1 loot!\n")
        elif count < 5:
            user.loot(3)
            print("Jackpot, +3 loot!\n")
        else:
            user.getHand().printCardListNames()
            user.chooseDiscard(1, user)
            print("Bad trip, -1 loot!\n")
        user.subtractTapped()
        return

def createPillsCards():
    pillsDeck = Deck([])
    yellow_pill = PillsYellow("Pills! (Y)", "test image.jpg")
    pillsDeck.addCardTop(yellow_pill)
    red_pill = PillsRed("Pills! (R)", "test image.jpg")
    pillsDeck.addCardTop(red_pill)
    blue_pill = PillsBlue("Pills! (B)", "test image.jpg")
    pillsDeck.addCardTop(blue_pill)
    return pillsDeck

# Choose a player, prevent the next 1 damage they would take this turn
class SoulHeart(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name

    def use(self, user):
        # choose a character to prevent 1 damage they would take this turn
        room = user.getRoom()
        room.displayCharacters()
        index = int(input("Who do you want to choose for Soul Heart?"))
        reduceDamage = ReduceDamage(1)
        character = room.getEntity(index)
        character.addInventory(reduceDamage)
        return

def createSoulHeartCards():
    soulHeartDeck = Deck([])
    soul_heart = SoulHeart("Soul Heart", "test image.jpg")
    soulHeartDeck.addCardTop(soul_heart)
    return soulHeartDeck

# "change the result of a dice roll to a number of your choosing"
class TheMagician(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        room = user.getRoom()
        stack = room.getStack()
        dice = stack.findDice()
        if isinstance(dice, Dice) == True:
            val = int(input("What do you want to change to roll to?: "))
            dice.setResult(val)
        else:
            print("No dice!\n")
        user.subtractTapped()
        return

# choose a player or monster then roll: deal damage ot them equal to the result
class TheHighPriestess(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        room = user.getRoom()
        playerList = room.getPlayers()
        room.displayEntities()
        target = int(input("Target which creature with THE HIGH PRIESTESS?: "))
        count = rollDice(user)
        # bomb the selected target
        if int(target) <= len(playerList):  # bomb player
            room.getPlayers()[int(target) - 1].takeDamage(count, user)
        else:  # bomb monster
            user.getBoard().getMonsters()[int(target) - 1 - len(playerList)][-1].takeDamage(count, user)
        user.subtractTapped()
        return

# Look at the top 5 cards from the Monster Deck, put 1 on top then the rest on the bottom
class TheEmperor(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name

    def use(self, user):
        deck = Deck([])
        room = user.getRoom()
        deck = user.drawMonster(5)
        # List the top 5 cards
        deck.printCardListNames()
        index = int(input(f'Which card do you want to return to the top of the monster deck: '))
        # put th chosen card to the top of the monster deck
        room.getBoard().getMonsterDeck().addCardTop(deck.getCard(index - 1))
        deck.removeCardIndex(index - 1)
        # add the cards back to the bottom of monster deck
        for i in range(deck.getDeckLength()):
            room.getBoard().getMonsterDeck().addCardBottom(deck.getCard(0))
            deck.removeCardIndex(0)
        return

# Choose a player or monster, prevent the next instance up to 2 damage they would take this turn
class TheHierophant(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name

    def use(self, user):
        # choose an entity to protect from an instance of up to 2 damage
        room = user.getRoom()
        room.displayEntities()
        index = int(input("Who do you want to choose for The Hierophant?"))
        reduceDamage = ReduceDamage(2)
        # if chosen entity is a monster
        if isinstance(room.getEntity(index), Enemy):
            # add the reduced damage to the enemy's inventory
            enemy = room.getEntity(index)
            enemy.addInventory(reduceDamage)
        else:
            # if not an enemy, then add the reduce damage to the characters inventory
            character = room.getEntity(index)
            character.addInventory(reduceDamage)
        return

# choose a player they gain 2 hp till end of turn
class TheLovers(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        room = user.getRoom()
        playerList = room.getPlayers()
        room.displayCharacters()
        target = int(input("Give 2 HP to which player?: "))
        target -= 1
        hp = playerList[target].getHp()
        playerList[target].setHp(hp + 2)
        user.subtractTapped()
        return

# choose a player they gain 1 hp and attack till end of turn
class TheChariot(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        room = user.getRoom()
        playerList = room.getPlayers()
        room.displayCharacters()
        target = int(input("Give HP and attack to which player?: "))
        target -= 1
        hp = playerList[target].getHp()
        attack = playerList[target].getAttack()
        playerList[target].setHp(hp + 1)
        playerList[target].setAttack(attack + 1)
        user.subtractTapped()
        return

# choose a player loot and gain cent until you have the same number of each as they do
class Justice(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        room = user.getRoom()
        playerList = room.getPlayers()
        room.displayCharacters()
        target = int(input("Copy loot and cent from which player?: "))
        target -= 1
        target = playerList[target]
        userCoins = user.getCoins()
        targetCoins = target.getCoins()
        if userCoins < targetCoins:
            diff = targetCoins - userCoins
            user.addCoins(diff)
        userLoot = user.getHand().getDeckLength()
        targetLoot = target.getHand().getDeckLength()
        if userLoot < targetLoot:
            diff = targetLoot - userLoot
            user.loot(diff)
        user.subtractTapped()
        return

# Look at the top 5 cards from the Treasure Deck, put 1 on top then the rest on the bottom
class TheHermit(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name

    def use(self, user):
        deck = Deck([])
        room = user.getRoom()
        deck = user.drawTreasure(5)
        # List the top 5 cards
        deck.printCardListNames()
        index = int(input(f'Which card do you want to return to the top of the treasure deck: '))
        # put th chosen card to the top of the treasure deck
        room.getBoard().getTreasureDeck().addCardTop(deck.getCard(index - 1))
        deck.removeCardIndex(index - 1)
        # add the cards back to the bottom of treasure deck
        for i in range(deck.getDeckLength()):
            room.getBoard().getTreasureDeck().addCardBottom(deck.getCard(0))
            deck.removeCardIndex(0)
        return

# roll --
class WheelOfFortune(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        count = rollDice(user)
        if count == 1:
            user.addCoins(1)
        elif count == 2:
            user.takeDamage(2, user)
        elif count == 3:
            user.loot(3)
        elif count == 4:
            user.addCoins(4)
        elif count == 5:
            user.addCoins(5)
        else:
            user.gainTreasure(1)
        user.subtractTapped()
        return

# choose a player, they gain 1 attack this turn and may attack an additional time this turn
class Strength(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        room = user.getRoom()
        playerList = room.getPlayers()
        room.displayCharacters()
        target = int(input("Give strength to which player?: "))
        target -= 1
        target = playerList[target]
        attack = target.getAttack()
        target.setAttack(attack + 1)
        target.getCharacter().addAttacksLeft()
        user.subtractTapped()
        return

# Look at the top card of each deck, you may put them at the bottom of their deck, then loot 2
class TheHangedMan(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name

    def use(self, user):
        board = user.getRoom().getBoard()
        # get and show the top loot card
        lootCard = board.getLootDeck().deal()
        lootCardChoice = int(input(f"{lootCard.getName()}\nDo you want to put this at the bottom of the Loot Deck?"
                                   f"\n1. Yes\n2. No\nChoice: "))
        # if chooses to put at bottom of loot deck, then do that
        if lootCardChoice == 1:
            board.getLootDeck().addCardBottom(lootCard)
        # else put the card back on top of loot deck
        else:
            board.getLootDeck().addCardTop(lootCard)
        # get and show the top treasure card
        treasureCard = board.getTreasureDeck().deal()
        treasureCardChoice = int(input(f"{treasureCard.getName()}\nDo you want to put this at the bottom of the "
                                       f"Treasure Deck? \n1. Yes\n2. No\nChoice: "))
        # if chooses to put at bottom of treasure deck, then do that
        if treasureCardChoice == 1:
            board.getTreasureDeck().addCardBottom(treasureCard)
        # else put the card back on top of treasure deck
        else:
            board.getTreasureDeck().addCardTop(treasureCard)
        # get and show the top monster card
        monsterCard = board.getMonsterDeck().deal()
        monsterCardChoice = int(input(f"{monsterCard.getName()}\nDo you want to put this at the bottom of the Monster "
                                      f"Deck?\n1. Yes\n2. No\nChoice: "))
        # if chooses to put at bottom of monster deck, then do that
        if monsterCardChoice == 1:
            board.getMonsterDeck().addCardBottom(monsterCard)
        # else put the card back on monster of loot deck
        else:
            board.getMonsterDeck().addCardTop(monsterCard)
        # after, loot 2
        user.loot(2)
        return

# kill a player
class Death(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        room = user.getRoom()
        playerList = room.getPlayers()
        room.displayCharacters()
        target = int(input("Give strength to which player?: "))
        target -= 1
        target = playerList[target]
        target.getCharacter().die(user)
        user.subtractTapped()
        return

# take 1 damage and gain 4c | take 2 damage and gain 8c
class Temperance(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        choice = int(input("Take 1 or 2 damage for reward?: "))
        if choice == 1:
            user.takeDamage(1, user)
            user.addCoins(4)
        else:
            user.takeDamage(2, user)
            user.addCoins(8)
        user.subtractTapped()
        return

# destroy an item you control, if you do, steal a non eternal item from a player or from the shop
class TheDevil(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        board = user.getRoom().getBoard()
        players = user.getRoom().getPlayers()
        if user.getItems().getDeckLength() < 1:
            user.subtractTapped()
            return
        choice = int(input("Steal from another player ('1') or from the shop ('2')?: "))
        items = user.getItems()
        items.printCardListNames()
        itemIndex = int(input("Destroy which of your own items?: "))
        itemIndex -= 1
        board.discardTreasure(user, itemIndex)
        if choice == 1: # steal from player
            user.getRoom().displayCharacters()
            choice2 = int(input("Steal from which player?: "))
            choice2 -= 1
            if players[choice2].getItems().getDeckLength() > 0: # so long as the chosen player has at least 1 item
                players[choice2].getItems().printCardListNames()
                itemChoice = int(input(f"Steal which item from player {choice2+1}?: "))
                itemChoice -= 1
                stolenItem = players[choice2].getItems().removeCardIndex(itemChoice)
                user.getItems().addCardTop(stolenItem)
        else:
            board.displayActiveTreasures()
            choice2 = int(input("Steal which item?: "))
            user.purchase(choice2)
        user.subtractTapped()
        return

# roll: each player takes 1 damage | each monster takes 1 damage | each player takes 2 damage
class TheTower(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        count = rollDice(user)
        players = user.getRoom().getPlayers()
        monsters = user.getRoom().getBoard().getMonsters()
        if count < 3:
            for i in range(len(players)):
                user.dealDamage(1, players[i])
            print("All players take 1 damage!\n")
        elif count < 5:
            for i in range(len(monsters)):
                user.dealDamage(1, monsters[i][-1])
            print("All monsters take 1 damage!\n")
        else:
            for i in range(len(players)):
                user.dealDamage(2, players[i])
            print("All players take 2 damage!!\n")
        user.subtractTapped()
        return

# gain +1 treasure
class TheStars(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        user.gainTreasure(1)
        user.subtractTapped()
        return

# Look at the top 5 cards from the Loot Deck, put 1 on top then the rest on the bottom
class TheMoon(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name

    def use(self, user):
        deck = Deck([])
        room = user.getRoom()
        deck = user.drawLoot(5)
        # List the top 5 cards
        deck.printCardListNames()
        index = int(input(f'Which card do you want to return to the top of the loot deck: '))
        # put th chosen card to the top of the loot deck
        room.getBoard().getLootDeck().addCardTop(deck.getCard(index - 1))
        deck.removeCardIndex(index - 1)
        # add the cards back to the bottom of loot deck
        for i in range(deck.getDeckLength()):
            room.getBoard().getLootDeck().addCardBottom(deck.getCard(0))
            deck.removeCardIndex(0)
        return

# choose a player who controls the most souls or is tied with the most. that player destroys a soul they control
class Judgement(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        most = 0
        mostPlayer = [] # contains the player number of each player with the most souls
        players = user.getRoom().getPlayers()
        # find the player with the most souls
        for i in range(len(players)):
            # if player i has the most souls so far
            if (players[i].getSouls() >= most):
                # if player i has a new record for most souls
                if most < players[i].getSouls():
                    most = players[i].getSouls()
                    # clear the players with less souls from mostPlayer
                    mostPlayer = []
                    mostPlayer.append(players[i].getNumber())
        if most == 0: # no one has any souls
            print("No one had any souls to discard.\n")
            return
        print("Choose a player to discard a soul.\n")
        for i in range(len(mostPlayer)):
            print(f"{i+1}: Player {mostPlayer[i]}")
        choice = int(input("Choice: "))
        choice -= 1
        # remove soul from chosen player
        chosenPlayer = players[mostPlayer[choice] - 1]
        chosenPlayer.subtractSouls(1)
        print(f"Player {choice + 1} was forced to discard a soul!\n")
        user.subtractTapped()
        return

# Look at each players hand, then loot 2
class TheWorld(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name

    def use(self, user):
        room = user.getRoom()
        # Shows each players hand
        print("Which player do you want to swap a card with")
        for i in range(len(room.getPlayers())):
            if room.getPlayers()[i].getCharacter().getName() == user.getCharacter().getName():
                pass  # skip showing player who used this card hands
            else:
                # show the other players hands
                print(f'{room.getPlayers()[i].getCharacter().getName()} Hand: ')
                room.getPlayers()[i].getHand().printCardListNames()
        # after seeing all players hands, loot 2
        user.loot(2)

def createTarotCards():
    tarotDeck = Deck([])
    the_magician = TheMagician("1. The Magician", "test image.jpg")
    for i in range(8): # TODO: there should only be 1 magician card in the deck, but this is for testing
        tarotDeck.addCardTop(the_magician)
    the_high_priestess = TheHighPriestess("2. The High Priestess", "test image.jpg")
    tarotDeck.addCardTop(the_high_priestess)

    the_emperor = TheEmperor("4. The Emperor", "test image.jpg")
    tarotDeck.addCardTop(the_emperor)
    the_hierophant = TheHierophant("5. The Hierophant", "test image.jpg")
    tarotDeck.addCardTop(the_hierophant)
    the_lovers = TheLovers("6. The Lovers", "test image.jpg")
    tarotDeck.addCardTop(the_lovers)
    the_chariot = TheChariot("7. The Chariot", "test image.jpg")
    tarotDeck.addCardTop(the_chariot)
    justice = Justice("8. Justice", "test image.jpg")
    tarotDeck.addCardTop(justice)
    the_hermit = TheHermit("9. The Hermit", "test image.jpg")
    tarotDeck.addCardTop(the_hermit)
    wheel_of_fortune = WheelOfFortune("10. Wheel of Fortune", "test image.jpg")
    tarotDeck.addCardTop(wheel_of_fortune)
    strength = Strength("11. Strength", "test image.jpg")
    tarotDeck.addCardTop(strength)
    the_hanged_man = TheHangedMan("12. The Hanged Man", "test image.jpg")
    tarotDeck.addCardTop(the_hanged_man)
    death = Death("13. Death", "test image.jpg")
    tarotDeck.addCardTop(death)
    temperance = Temperance("14. Temperance", "test image.jpg")
    tarotDeck.addCardTop(temperance)
    the_devil = TheDevil("15. The Devil", "test image.jpg")
    tarotDeck.addCardTop(the_devil)
    the_tower = TheTower("16. The Tower", "test image.jpg")
    tarotDeck.addCardTop(the_tower)
    the_stars = TheStars("17. The Stars", "test image.jpg")
    tarotDeck.addCardTop(the_stars)
    the_moon = TheMoon("18. The Moon", "test image.jpg")
    tarotDeck.addCardTop(the_moon)
    judgement = Judgement("20. Judgement", "test image.jpg")
    tarotDeck.addCardTop(judgement)
    the_world = TheWorld("21. The World", "test image.jpg")
    tarotDeck.addCardTop(the_world)
    return tarotDeck

# put each monster not being attacked into discard and replace each with the top card of the monster deck
class Ehwaz(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        monsters = user.getBoard().getMonsters()
        # for each monster slot on the board
        for i in range(len(monsters)):
            # for each monster in the monster slot
            for j in range(len(monsters[i])):
                while len(monsters[i]) > 0:
                    user.getBoard().discardMonsterIndex(i)
        user.getBoard().checkMonsterSlots(user)
        user.subtractTapped()
        return

# roll for 1 of 6 unique effects
class BlankRune(Loot):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    def getName(self):
        return self.name
    
    def getJsonObject(self):
        obj = {
            "card": super().getJsonObject()
        }
        return obj

    def use(self, user):
        result = rollDice(user)
        players = user.getRoom().getPlayers()
        numPlayers = len(players)
        nextPlayerNum = user.getNumber()
        if result == 1:
            print("Everyone gains 1c (yawn).\n")
            for i in range(len(players)):
                players[nextPlayerNum - 1].addCoins(1)
                nextPlayerNum = (nextPlayerNum + 1) % numPlayers
        elif result == 2:
            print("Everyone draws 2 loot.\n")
            for i in range(len(players)):
                players[nextPlayerNum - 1].loot(2)
                nextPlayerNum = (nextPlayerNum + 1) % numPlayers
        elif result == 3:
            print("Everyone takes 3 damage D: !\n")
            for i in range(len(players)):
                players[nextPlayerNum - 1].takeDamage(3, user)
                nextPlayerNum = (nextPlayerNum + 1) % numPlayers
        elif result == 4:
            print("Everyone gets 4c.\n")
            for i in range(len(players)):
                players[nextPlayerNum - 1].addCoins(4)
                nextPlayerNum = (nextPlayerNum + 1) % numPlayers
        elif result == 5:
            print("Everyone gets 5 loot!.\n")
            for i in range(len(players)):
                players[nextPlayerNum - 1].loot(5)
                nextPlayerNum = (nextPlayerNum + 1) % numPlayers
        else:
            print("Everyone gets 6c!\n")
            for i in range(len(players)):
                players[nextPlayerNum - 1].addCoins(6)
                nextPlayerNum = (nextPlayerNum + 1) % numPlayers
        user.subtractTapped()
        return

def createRuneCards():
    runeDeck = Deck([])
    ehwaz = Ehwaz("Ehwaz", "test image.jpg")
    runeDeck.addCardTop(ehwaz)
    blank_rune = BlankRune("Blank Rune", "test image.jpg")
    runeDeck.addCardTop(blank_rune)
    return runeDeck



def createAllLootCards():
    lootM = createMoneyCards()
    lootB = createBombCards()
    lootD = createDiceShardCards()
    lootMB = createMegaBatteryCards()
    lootP = createPillsCards()
    lootSH = createSoulHeartCards()
    lootT = createTarotCards()
    lootR = createRuneCards()
    # add all the loot cards to the same deck
    allLoot = Deck([])
    allLoot.combineDeck(lootM)
    allLoot.combineDeck(lootB)
    allLoot.combineDeck(lootD)
    allLoot.combineDeck(lootMB)
    allLoot.combineDeck(lootP)
    allLoot.combineDeck(lootSH)
    allLoot.combineDeck(lootT)
    allLoot.combineDeck(lootR)
    #allLoot.shuffle()
    return allLoot
