# Contributors: Jackson Cashman
'''
Players are contained in a Room
Player can access their Room
Players can access their Character
'''
from Cards import Character
from Decks import Deck
from LootReward import LootReward
from TreasureReward import TreasureReward
from LootCards import *
from Characters import *
from TreasureCards import *
from SilverTreasureCards import *

class Player:
    def __init__(self, character, num, room):
        self.character = character
        self.num = num
        self.room = room
        self.coins = 10 # players always have 3 coins at the start of the game
        self.hand = Deck([])
        # self.hand = createAllLootCards() # all loot cards are in player hand for debug purposes
        self.items = Deck([])
        # #self.items = createAllStartingItems()
        # self.items = createTreasureCards()
        #self.items.combineDeck(createDiceEffectTreasures())
        #self.items.combineDeck(createAllStartingItems())
        self.souls = 0

    # getters

    def getCharacter(self):
        return self.character

    def getNumber(self):
        return self.num

    def getHand(self):
        return self.hand

    def getItems(self):
        return self.items

    def getInventory(self):
        return self.inventory

    def getCoins(self):
        return self.coins

    def getSouls(self):
        return self.souls

    def getStack(self):
        return self.room.getStack()

    def getRoom(self):
        return self.room

    def getBoard(self):
        return self.room.getBoard()

    def getTapped(self):
        return self.character.getTapped()

    def getMaxHp(self):
        return self.character.getMaxHp()

    def getHp(self):
        return self.character.getHp()

    def getAttack(self):
        return self.character.getAttack()
    
    def getJsonObject(self):
        playerObject = {
            "playerNumber": self.num,
            "username": "need to add in constructor (Player.py)",
            "coins": self.coins,
            "souls": self.souls,
            "items": self.items.getJsonObject(),
            "hand": self.hand.getJsonObject(),
            "curses": "TBD (from Player.py)",
            "character": self.character.getJsonObject()
        }
        return playerObject

    # setters

    def setMaxHp(self, num):
        self.character.setMaxHp(num)
        return

    def setHp(self, num):
        self.character.setHp(num)
        return

    def setAttack(self, num):
        self.character.setAttack(num)
        return

    def setHand(self, hand):
        self.hand = hand

    def setCoins(self, num):
        self.coins = num

    # other functions

    # draw num cards into the player's hand
    def loot(self, num):
        for i in range(num):
            lootCard = self.getBoard().getLootDeck().deal()
            self.hand.addCardTop(lootCard)
        return

    # add cards to players item deck
    def gainTreasure(self, num):
        for i in range(num):
            treasureCard = self.getBoard().getTreasureDeck().deal()
            self.items.addCardTop(treasureCard)
            # the treasure has no tag, return
            if isinstance(treasureCard, PlainSilverTreasure):
                return
            # the treasure must have a tag, add that card to global effects
            board = self.getBoard()
            board.getGlobalEffects().append([treasureCard, self])
        return

    # silver treasure --> plain silver treasure
    #                     dice effect treasure

    # used to check what is on top of a deck (not adding to hand)
    def drawLoot(self, num):
        deck = Deck([])
        for i in range(num):
            deck.addCardTop(self.getBoard().getLootDeck().deal())
        return deck

    # used to check what is on top of a deck (not adding to item list)
    def drawTreasure(self, num):
        # just return 1 card if only want 1
        if num == 1:
            return self.getBoard().getTreasureDeck().deal()
        # return a deck of cards if want multiple
        else:
            deck = Deck([])
            for i in range(num):
                deck.addCardTop(self.getBoard().getTreasureDeck().deal())
            return deck

    # used to check what is top of deck
    def drawMonster(self, num):
        deck = Deck([])
        for i in range(num):
            deck.addCardTop(self.getBoard().getMonsterDeck().deal())
        return deck

    # choose num loot cards from your hand to discard
    # use the dicardLoot funct in Baord with this to put it in the discard deck
    # this should only be used to discard one card at a time so num is pointless
    def chooseDiscard(self, num, player):
        for i in range(num):
            inp = int(input("Which card do you want to discard? "))
            return player.getHand().removeCardIndex(inp)


    # add the shop treasure in the specified index to the players collection
    def purchase(self, slotNum):
        treasureCard = self.getBoard().getTreasure(slotNum)
        self.items.addCardTop(treasureCard)
        # the treasure has no tag, return
        if isinstance(self.getBoard().getTreasure(slotNum), PlainSilverTreasure):
            return
        # the treasure must have a tag, add that card to global effects
        board = self.getBoard()
        board.getGlobalEffects().append([treasureCard, self])
        self.getBoard().clearTreasureSlot(slotNum)
        self.getBoard().checkTreasureSlots()
        return

    def useLoot(self, loot):
        loot.use(self)
        return

    def addSouls(self, num):
        self.souls += num
        return

    def subtractSouls(self, num):
        self.souls -= num
        return

    def addCoins(self, num):
        self.coins += num
        return

    def addHp(self, num):
        self.character.setHp(self.character.getHp() + num)
        return

    def addAttack(self, num):
        self.character.setAttack(self.character.getAttack() + num)
        return

    def subtractCoins(self, num):
        self.coins -= num
        if self.coins < 0:
            self.coins = 0
        return

    def subtractTapped(self):
        self.character.subtractTapped()
        return

    # this function is necessary to facilitate effects that proc when dealing damage
    # also is present in Entity
    def dealDamage(self, num, target):
        targetHp = target.getHp()
        target.takeDamage(num, self)
        # make sure that damage was not prevented before carrying out damage procs
        if target.getHp() == targetHp:
            self.damageEffect(target)
        return

    def damageEffect(self, target):
        return

    def takeDamage(self, num, attacker):
        hpBefore = self.getCharacter().getHp()
        self.character.takeDamage(num, attacker)
        hpAfter = self.getCharacter().getHp()
        # check to see if the character took damage
        if hpBefore > hpAfter:
            # check for "take damage" effects in globalEffects
            globalEffects = self.getBoard().getGlobalEffects()
            for i in range(len(globalEffects)):
                # if the player's character took damage
                if isinstance(globalEffects[i][0], TakeDamageTreasure):
                    itemUser = globalEffects[i][1]
                    if self.getNumber() == itemUser.getNumber():
                        itemUser.addToStack(globalEffects[i][0])
                        itemUser.getRoom().useDamageEffect(itemUser.getNumber(), hpBefore - hpAfter)
        return

    # play something that belongs to the player (Loot, Treasure, Dice, etc)
    def addToStack(self, obj):
        player = self
        # when something is added to the stack, a player number is attached to it
        self.getRoom().addToStack([obj, player])
        return

    def addToItems(self, card):
        self.items.addCardBottom(card)
        return

