# Contributors: Jackson Cashman
# Contributor: Daniel De Guzman - getJsonObject()
"""
This file contains the class definitions for all card types and interfaces
Classes for more specific cards (such as functional Loot cards) are in their individual python files
"""
import json
from Coins import CoinStack
from TreasureReward import TreasureReward

# from Dice import Dice
from DeclareAttack import DeclaredAttack
from Effects import *
from JsonOutputHelper import JsonOutputHelper

Json = JsonOutputHelper()
"""
# this assigns a picture to an Image obj and then opens it
# images should be defined using Image.open() and then passed into the init for Card (i think)
myImage = Image.open("test image.jpg")
myImage.show()
"""


# Card is the parent class of all classes in this file
# name: string
# picture: tbd photo file
class Card:
    def __init__(self, name, picture):
        self.name = name
        self.picture = picture

    def getName(self):
        return self.name

    def getPicture(self):
        return self.picture

    # returns the JSON object for the class - D.D.
    # used for frontend rendering/gamestates - D.D.
    def getJsonObject(self):
        cardObject = {"name": self.name, "picture": self.picture}
        return cardObject


# Card child class for Entity
# maxHp: int
# hp: int
# attack: int
class Entity(Card):
    def __init__(self, name, picture, maxHp, attack):
        super().__init__(name, picture)
        self.maxHp = maxHp
        self.hp = maxHp
        self.attack = attack
        self.maxAttack = attack
        self.inventory = (
            []
        )  # this can be used to keep track of buffs that last toll end of turn, may change later

    # getters

    def getMaxHp(self):
        return self.maxHp

    def getHp(self):
        return self.hp

    def getAttack(self):
        return self.attack

    def getMaxAttack(self):
        return self.maxAttack

    def getInventory(self):
        return self.inventory

    def getJsonObject(self):
        entityObject = {
            "card": super().getJsonObject(),
            "hp": self.hp,
            "maxHp": self.maxHp,
            "attack": self.attack,
            "maxAttack": self.maxAttack,
            # don't think we need inventory anymore - D.D.
            # "inventory": self.inventory
        }
        return entityObject

    # setters

    def setMaxHp(self, num):  # i dont think this will ever be used
        self.maxHp = num
        return

    def setHp(self, num):
        self.hp = num
        return

    def setMaxAttack(self, num):
        self.maxAttack = num
        return

    def setAttack(self, num):
        self.attack = num
        return

    # other functions

    # add temporary buffs to a entity inventory
    def addInventory(self, buff):
        self.inventory.append(buff)
        return

    # this function can be used at the end of each turn to remove all temporary buffs
    def clearInventory(self):
        self.inventory = []
        return

    def clearEffect(self, index):
        # self.inventory.remove()
        self.inventory.pop(index)
        return

    # this function is necessary to facilitate effects that proc when dealing damage
    # also is present in Player
    def dealDamage(self, num, target):
        targetHp = target.getHp()
        target.takeDamage(num, self)
        # make sure that damage was not prevented before carrying out damage procs
        if target.getHp() < targetHp:
            self.damageEffect(target)
        return

    def damageEffect(self, target):
        # overwritten in specific monster classes
        return

    # Entity will take num damage
    # Entity hp cannot go below 0
    # attacker is another entity
    def takeDamage(self, num, attacker):
        # cant take more damage if already dead
        if self.hp <= 0:
            return
        # Look through character being attacked inventory to check for ReduceDamage effect
        if len(self.inventory) != 0:
            inventoryLength = len(self.inventory)
            for i in range(len(self.inventory)):
                if isinstance(self.inventory[inventoryLength - i - 1], ReduceDamage):
                    num = self.inventory[inventoryLength - i - 1].effect(num)
                    self.clearEffect(inventoryLength - i - 1)
                    # if user isn't going to take any damage, then stop the loop since not needed, dont want to destroy
                    # unused ReduceDamage
                    if num == 0:
                        break
        self.hp -= num
        if self.hp <= 0:
            # death
            if isinstance(self, Enemy):
                self.die(attacker)
        if isinstance(self, Enemy):
            activeMonsters = attacker.getRoom().getBoard().getMonsters()
            Json.monsterOutput(activeMonsters)
        return


# Character child class for Entity(Card)
# tapped: int, the value in "tapped" is how many loot cards this character can play this turn
# attacksLeft: int, the value in "attacksLeft" is how many attacks this character can initiate this turn
# purchases: int, the value in "purchases" is how many items the character can buy from the shop this turn
class Character(Entity):
    def __init__(self, name, picture, maxHp, attack):
        super().__init__(name, picture, maxHp, attack)
        self.hp = maxHp
        self.maxAttack = attack
        # range from 0-2. 2 means it is your turn and can play both your free and 'tapped' loot play
        # gets reduced to 1 at the end of your turn
        # self.tapped = 0
        self.tapped = 1  # TODO: this should be 0 but is set to 1 for testing purposes
        self.attacksLeft = 0
        self.purchases = 0
        self.mandatoryAttacks = (
            0  # the number of times the character must attack again this turn
        )
        self.mandatoryDeckAttacks = 0  # the number of times the character must attack the unknown monster slot this turn

    # getters

    def getTapped(self):
        return self.tapped

    def getPurchases(self):
        return self.purchases

    def getAttacksLeft(self):
        return self.attacksLeft

    def getJsonObject(self):
        characterObject = {
            "entity": super().getJsonObject(),
            "tapped": self.tapped,
            "attacksLeft": self.attacksLeft,
            "purchases": self.purchases,
            "mandatoryAttacks": self.mandatoryAttacks,
        }
        return characterObject

    def getMandatoryAttacks(self):
        return self.mandatoryAttacks

    def getMandatoryDeckAttacks(self):
        return self.mandatoryDeckAttacks

    # setters

    def setTapped(self, num):
        self.tapped = num
        if num < 0:
            raise ValueError("Attribute 'tapped' should not go below 0!")
        return

    def setAttacksLeft(self, num):
        self.attacksLeft = num
        if num < 0:
            raise ValueError("Attribute 'attacksLeft' should not go below 0!")
        return

    def setPurchases(self, num):
        self.purchases = num
        if num < 0:
            raise ValueError("Attribute 'purchases' should not go below 0!")
        return

    # other functions

    def subtractTapped(self):
        self.tapped -= 1
        return

    def addAttacksLeft(self):
        self.attacksLeft += 1
        return

    def addMandatoryAttacks(self):
        self.mandatoryAttacks += 1
        self.attacksLeft += 1
        return

    def addMandatoryDeckAttacks(self):
        self.mandatoryDeckAttacks += 1
        return

    def subtractAttacksLeft(self):
        self.attacksLeft -= 1
        return

    def subtractMandatoryAttacks(self):
        self.mandatoryAttacks -= 1
        return

    def subtractMandatoryDeckAttacks(self):
        self.mandatoryDeckAttacks -= 1
        return

    def addPurchases(self):
        self.purchases += 1
        return

    def subtractPurchases(self):
        self.purchases -= 1
        return


# Monster child interface for Entity(Card)
class Monster(Card):
    def __init__(self, name, picture):
        super().__init__(name, picture)


# Enemy child class for Monster(Card) and Entity(Card)
# There will be many child classes from this class for each kind of Monster
# diceValue: int
# soulCount: int
# reward: list (may be variable amounts of loot, coins, or treasure)
class Enemy(Entity, Monster):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack)
        self.hp = maxHp
        self.maxAttack = attack
        self.diceValue = diceValue
        self.soulCount = soulCount
        self.reward = reward

    # getters

    def getDiceValue(self):
        return self.diceValue

    def getSoulCount(self):
        return self.soulCount

    def getReward(self):
        return self.reward

    def getJsonObject(self):
        enemyObject = {
            "entity": super().getJsonObject(),
            "diceValue": self.diceValue,
            "soulCount": self.soulCount,
        }
        return enemyObject

    # setters

    def setDiceValue(self, num):
        self.diceValue = num
        return

    def setSoulCount(self, num):  # not sure if this will ever have any use
        self.soulCount = num
        return

    def setReward(
        self, lis
    ):  # adding a function to add rewards to an existing reward might be easier once cards are implemented
        self.reward = lis
        return

    # other functions

    # TODO: make souls attached to actual cards (important for when a player must discard a soul card)
    def addSouls(self, num):
        self.soulCount += num
        return

    # TODO: rewards should always go to the active player, but the player who dealt lethal damage is also sometimes needed
    # give awards for killing monster
    # takes the attacking player as a parameter
    def die(self, player):
        message = f"{self.getName()} has died!"
        Json.systemOutput(message)
        self.hp = 0
        # find the active player
        activePlayer = player.getRoom().getActivePlayer()
        # claim rewards
        from LootReward import LootReward

        for i in range(len(self.getReward())):
            # award Coin rewards
            if isinstance(self.getReward()[i], CoinStack):
                coinCount = self.getReward()[i].getCount()
                activePlayer.addCoins(coinCount)
            # award Loot rewards
            elif isinstance(self.getReward()[i], LootReward):
                lootCount = self.getReward()[i].getCount()
                activePlayer.loot(lootCount)
            # award Treasure rewards
            elif isinstance(self.getReward()[i], TreasureReward):
                treasureCount = self.getReward()[i].getCount()
                activePlayer.gainTreasure(treasureCount)
        # award souls
        if self.getSoulCount() > 0:
            # award soul rewards
            soulValue = self.getSoulCount()
            activePlayer.addSouls(soulValue)
        # monster death effects trigger
        self.dieEffect(player)

        # discard monster and replace empty slots
        index = player.getBoard().findMatchingMonster(self.getName())
        player.getBoard().discardMonsterIndex(index)
        player.getBoard().checkMonsterSlots(player)

        # remove the monster and attack roll from the stack (relevant if it dies to a bomb mid combat)
        stack = player.getRoom().getStack().getStack()
        if len(stack) == 0:
            return  # stack is empty so have this to avoid an error
        if isinstance(stack[0][0], DeclaredAttack):
            if stack[0][0].getMonster() == self:
                stack.pop(0)
                # if the stack is empty
                if len(stack) == 0:
                    return
                # if there is still an attack roll/bomb on the stack
                stack.pop(0)
        return

    # basic enemies have no die effect
    def dieEffect(self, player):
        return


# Event child class of Monster(Card)
# There will be many child classes from this class for each kind of Event
class Event(Monster):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    # event cards should conclude their use functions with resolve to be discarded
    def resolve(self, activePlayer):
        board = activePlayer.getBoard()
        index = board.findMatchingMonster(self.name)
        board.discardMonsterIndex(index)

        # Print Player Hand and Board for frontend rendering - D.D.
        playerList = activePlayer.getRoom().getPlayers()
        for player in playerList:
            Json.playerHandOutput(player)

        Json.playerBoardOutput(activePlayer)
        board.checkMonsterSlots(activePlayer)
        return


# TODO: Curse child class of Monster(Card)
# There will be many child classes from this class for each kind of Curse
class Curse(Monster):
    pass


# Loot child class for Card
# There will be many child classes from this class for each kind of Loot
class Loot(Card):
    def __init__(self, name, picture):
        super().__init__(name, picture)

    # this method is just a dummy and gets overwritten in the subclasses of Loot
    def use(self):
        pass


# Treasure child interface for Card
# eternal: bool (True is eternal, False is non-eternal)
class Treasure(Card):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture)
        self.eternal = eternal

    # getters

    def getEternal(self):
        return self.eternal

    # getJsonObject for GameState - D.D.
    def getJsonObject(self):
        treasureObject = {"card": super().getJsonObject(), "eternal": self.eternal}
        # Built in python function to check if an object has an attribute.
        if hasattr(self, "tapped"):
            treasureObject["tapped"] = self.tapped
        else:
            treasureObject["tapped"] = False
        return treasureObject

    # setters

    def setEternal(self, tf):
        if tf == True:
            self.eternal = True
        elif tf == False:
            self.eternal = False
        else:
            raise SyntaxError("setEternal input must be either 'True' or 'False'")
        return

    def discard(self):
        # do nothing, only want specific cards to implement this function
        return


# TODO: SilverTreasure child class for Treasure(Card)
# There will be many child classes from this class for each kind of SilverTreasure
# NO CARDS should have this as their most specialized class, silver treasures with no effects should the PlainSilverTreasure class
class SilverTreasure(Treasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)


# TODO: GoldTreasure child class for Treasure(Card)
# There will be many child classes from this class for each kind of GoldTreasure
# tapped: bool (False = untapped, True = tapped)
class GoldTreasure(Treasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.tapped = False

    # getters

    def getTapped(self):
        return self.tapped

    # set a GoldTreasure to be tapped or untapped
    # returns nothing
    def setTapped(self, tf):
        if tf == True:
            self.tapped = True
        else:
            self.tapped = False
        return


# TODO: BonusSoul child class for Card
# there will be several child classes from this class for each BonusSoul
class BonusSoul(Card):
    def __init__(self, achieved):
        self.achieved = achieved

    def getJsonObject(self):
        bonusSoulObject = {"card": super().getJsonObject(), "achieved": self.achieved}
        return bonusSoulObject

    # set a BonusSoul as achieved (once achieved a bonus soul can never be 'un-achieved' again)
    # returns nothing
    def achieve(self):
        self.achieved = True
        return


"""
Logic for soul heart
room = user.getRoom()
        room.displayEntities()
        index = int(input("Who do you want to choose for Yum Heart?"))
        entity = room.getEntity(index)
        entity.setHp(entity.getHp() + 1)
        self.tapped = True
"""
