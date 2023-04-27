# Contributors:
#    Jackson Cashman:
#        all functions EXCEPT: getPlayerHandObject, getPlayerBoardSectionObject, getJsonObject
#        getChosenPlayer, drawLoot, drawTreasure, drawMonster, getName
#    Ethan Sandoval:
#        getChosenPlayer, drawLoot, drawTreasure, drawMonster, getName
#    Daniel De Guzman:
#        getPlayerHandObject, getPlayerBoardSectionObject, getJsonObject
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
import sys
from Board import checkGuppySoul
from JsonOutputHelper import JsonOutputHelper

Json = JsonOutputHelper()

class Player:
    def __init__(self, character, num, room, socketId, username):
        self.character = character
        self.num = num
        self.room = room
        self.socketId = socketId
        self.username = username
        self.coins = 10 # players always have 3 coins at the start of the game
        # self.hand = Deck([])
        #self.hand = createBombCards()
        self.hand = createAllLootCards() # all loot cards are in player hand for debug purposes
        #self.items = Deck([])
        #self.items = createAllStartingItems()
        self.items = createTreasureCards()
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
    
    def getSocketId(self):
        return self.socketId
    
    def getUsername(self):
        return self.username

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
    
    def getPlayerHandObject(self):
        playerObject = {
            "messageFlag": "PLAYER-HAND",
            "socketID": self.socketId,
            "username": self.username,
            "playerNumber": self.num,
            "hand": self.hand.getJsonObject()
        }
        return playerObject
    
    def getPlayerBoardSectionObject(self):
        playerObject = {
            "messageFlag": "PLAYER-BOARD",
            "playerNumber": self.num,
            "character": self.character.getJsonObject(),
            "cardCount": self.hand.getDeckLength(),
            "coins": self.coins,
            "souls": self.souls,
            "items": self.items.getJsonObject(),
        }
        return playerObject
    
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

    def getName(self):
        return self.getCharacter().getName()

    # used to get a player that a user has chosen to do something to that player (like steal or destroy an item)
    # does not allow a player to choose themself
    def getChosenPlayer(self, message, user):
        room = user.getRoom()
        playerOption = []
        # create a deep copy so we can remove the user as an option to choose
        playerList = copy.deepcopy(room.getPlayers())
        for i in range(len(playerList)):
            if playerList[i].getNumber() == user.getNumber():
                playerList.pop(i)
                break
        # create an array of strings to pass into JSON
        for i in playerList:
            playerOption.append(i.getName())
        # this passes and prints data for JSON
        Json.choiceOutput(user.getSocketId(), message, playerOption)
        # then look for input from button press
        playerChoice = int(input())
        # return a shallow copy of chosen player
        for i in room.getPlayers():
            if i.getNumber() == playerList[playerChoice - 1].getNumber():
                return i
        # if don't return a player then an error has occurred
        raise "A player didn't get returned"

    # choose any player and return that player
    def chooseAnyPlayer(self, message):
        room = self.getRoom()
        playerList = room.getPlayers()
        playerOption = []
        # create an array of strings to pass into JSON
        for i in playerList:
            playerOption.append(i.getName())
        # this passes and prints data for JSON
        Json.choiceOutput(self.getSocketId(), message, playerOption)
        # then look for input from button press
        playerChoice = int(input())
        # return a shallow copy of chosen player
        for i in room.getPlayers():
            if i.getNumber() == playerList[playerChoice - 1].getNumber():
                return i
        # if don't return a player then an error has occurred
        raise "A player didn't get returned"

    # choose any entity and return it
    def chooseAnyEntity(self, message):
        entities = self.room.getEntities()
        playerOption = []
        # create an array of strings to pass into JSON
        for i in entities:
            playerOption.append(i.getName())
        # this passes and prints data for JSON
        Json.choiceOutput(self.getSocketId(), message, playerOption)
        # then look for input from button press
        playerChoice = int(input())
        return entities[playerChoice-1]

    # choose any active monster to attack, or the facedown monster, and return it
    def chooseAttackTarget(self, message):
        monsters = self.getBoard().getMonsters()
        playerOption = []
        # create an array of strings to pass into JSON
        for i in monsters:
            playerOption.append(i[-1].getName())
        playerOption.append("FACE DOWN MONSTER")
        # this passes and prints data for JSON
        Json.choiceOutput(self.getSocketId(), message, playerOption)
        # then look for input from button press
        playerChoice = int(input())
        if playerChoice <= len(monsters):
            return monsters[playerChoice - 1][-1]
        elif playerChoice == (len(monsters) + 1):
            return "face down monster"
        else:
            return "cancel"

    # choose any active treasure to purchase, or the facedown treasure, and return it
    def choosePurchaseTarget(self, message):
        treasures = self.getBoard().getTreasures()
        playerOption = []
        # create an array of strings to pass into JSON
        for i in treasures:
            playerOption.append(i[-1].getName())
        playerOption.append("FACE DOWN TREASURE")
        # this passes and prints data for JSON
        Json.choiceOutput(self.getSocketId(), message, playerOption)
        # then look for input from button press
        playerChoice = int(input())
        if playerChoice <= len(treasures):
            return treasures[playerChoice - 1][-1]
        elif playerChoice == (len(treasures) + 1):
            return "face down treasure"
        else:
            return "cancel"

    def chooseItemSteal(self):
        message = "Choose a player to steal an item from. >:)"
        chosenPlayer = self.getChosenPlayer(message, self)
        board = self.getBoard()
        # check to see if they have items
        if chosenPlayer.getItems().getDeckLength() <= 1:
            message = f"{chosenPlayer.getName()}'s has no items that can be stolen!"
            Json.systemOutput(message)
        else:
            message = f"Choose which of {chosenPlayer.getName()}'s items to steal."
            itemList = []
            # this should add every card from the player's items to a list, except for their eternal starting item
            # this relies on every item being added to the players Items being added with addCardTop()
            iter = 0
            for i in chosenPlayer.getItems().getCardList():
                # skip the last item (which we are assuming is eternal)
                if iter == len(chosenPlayer.getItems().getCardList()) - 1:
                    break
                treasure_i = i
                itemList.insert(0, treasure_i.getName())
                iter += 1
            Json.choiceOutput(self.getSocketId(), message, itemList)
            playerChoice = int(input())
            stealIndex = -playerChoice - 1 # -2 is to account of the difference from the index pov and the eternal item
            stolenTreasure = chosenPlayer.getItems().removeCardIndex(stealIndex)
            self.getItems().addCardTop(stolenTreasure)
            message = f"Player {self.getNumber()} stole an item from Player {chosenPlayer.getNumber()}!"
            Json.systemOutput(message)
        return


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
            # check if soul of gluttony should be awarded
            if (self.hand.getDeckLength() >= 10) and (self.getBoard().getSoulDict()['Gluttony'] is False):
                self.getBoard().getSoulDict()['Gluttony'] = True
                print(f"Player {self.num} achieved the Soul of Gluttony!\n")
                self.addSouls(1)
        # PLAYER-HAND JSON
        # PLAYER-BOARD JSON
        return

    # add cards to players item deck
    def gainTreasure(self, num):
        for i in range(num):
            treasureCard = self.getBoard().getTreasureDeck().deal()
            self.items.addCardTop(treasureCard)
            checkGuppySoul(treasureCard, self)
            # the treasure has no tag, return
            if isinstance(treasureCard, PlainSilverTreasure):
                return
            # the treasure must have a tag, add that card to global effects
            board = self.getBoard()
            board.getGlobalEffects().append([treasureCard, self])
        # PLAYER-BOARD JSON
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

    # use the discardTreasure funct in Board with this to put it in the discard deck
    def chooseDiscardTreasure(self, player):
        playerOption = []
        message = "Which treasure card do you want to discard?"
        for i in player.getItems().getCardList():
            playerOption.append(i.getName())
        Json.choiceOutput(player.getSocketId(), message, playerOption)
        inp = int(input())
        inp -= 1
        treasure = player.getItems().getCard(inp)
        player.getBoard().getDiscardTreasureDeck().addCardTop(treasure)
        return player.getItems().removeCardIndex(inp)

    # choose a loot card from your hand to discard
    # use the discardLoot funct in Board with this to put it in the discard deck
    # this should only be used to discard one card at a time so num is pointless
    def chooseDiscard(self, num, player):
        playerOption = []
        message = "Which loot card do you want to discard?"
        for i in player.getHand().getCardList():
            playerOption.append(i.getName())
        Json.choiceOutput(player.getSocketId(), message, playerOption)
        inp = int(input())
        inp -= 1
        loot = player.getHand().getCard(inp)
        player.getBoard().getDiscardLootDeck().addCardTop(loot)
        # PLAYER-HAND JSON
        return player.getHand().removeCardIndex(inp)

    # choose a loot card and return the index of that card in the player's hand
    def chooseLootIndex(self):
        playerOption = []
        message = "Select a Loot card"
        for i in self.getHand().getCardList():
            playerOption.append(i.getName())
        Json.choiceOutput(self.getSocketId(), message, playerOption)
        inp = int(input())
        inp -= 1
        return inp

    # choose a treasure card and return the index of that card in the player's item list
    def chooseTreasureIndex(self):
        playerOption = []
        message = "Select a Treasure card"
        for i in self.getItems().getCardList():
            playerOption.append(i.getName())
        Json.choiceOutput(self.getSocketId(), message, playerOption)
        inp = int(input())
        inp -= 1
        return inp




    # add the shop treasure in the specified index to the players collection
    def purchase(self, slotNum):
        numSlots = len(self.getBoard().getTreasures())
        # purchasing card from treasure slot
        if slotNum <= numSlots:
            treasureCard = self.getBoard().getTreasure(slotNum)
            self.items.addCardTop(treasureCard)
            checkGuppySoul(treasureCard, self)
            # the treasure has no tag, return
            if isinstance(self.getBoard().getTreasure(slotNum), PlainSilverTreasure):
                return
            if isinstance(self.getBoard().getTreasure(slotNum), GoldTreasure):
                return
            # the treasure must have a tag, add that card to global effects
            board = self.getBoard()
            board.getGlobalEffects().append([treasureCard, self])
            self.getBoard().clearTreasureSlot(slotNum)
            self.getBoard().checkTreasureSlots()
            return
        # purchasing face down treasure card
        else:
            # take the card off the deck and add it to the players collection
            treasureCard = self.getBoard().getTreasureDeck().deal()
            self.items.addCardTop(treasureCard)
            # the treasure has no tag, return
            if isinstance(treasureCard, PlainSilverTreasure):
                return
            if isinstance(treasureCard, GoldTreasure):
                return
            # the treasure must have a tag, add that card to global effects
            board = self.getBoard()
            board.getGlobalEffects().append([treasureCard, self])
            self.getBoard().checkTreasureSlots()
            return

    def useLoot(self, loot):
        loot.use(self)
        return

    def addSouls(self, num):
        self.souls += num
        if self.souls >= 4:
            message = f"Player {self.num} has won the game!!!"
            Json.systemOutput(message)
            sys.exit(0)
        return

    def subtractSouls(self, num):
        self.souls -= num
        return

    def addCoins(self, num):
        self.coins += num
        # award soul of greed if player has 25c and soul of greed has not been collected yet
        if (self.coins >= 25) and (self.getBoard().getSoulDict()['Greed'] is False):
            self.getBoard().getSoulDict()['Greed'] = True
            message = f"Player {self.num} achieved the Soul of Greed!\n"
            Json.systemOutput(message)
            self.addSouls(1)
        # PLAYER-BOARD JSON
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
        if target.getHp() < targetHp:
            self.damageEffect(target)
        return

    def damageEffect(self, target):
        return

    def takeDamage(self, num, attacker):
        hpBefore = self.getCharacter().getHp()
        # return early if player was already dead
        if hpBefore < 1:
            return
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
        if hpAfter < 1:
            self.die(attacker)
        return

    # player death
    def die(self, attacker):
        message = f"Player {self.num} has died!"
        Json.systemOutput(message)
        if self.coins > 0:
            message = f"Player {self.num} had 1 penny pilfered :("
            Json.systemOutput(message)
            self.coins -= 1
        if self.hand.getDeckLength() > 0:
            message = f"Player {self.num} had 1 loot lost :("
            Json.systemOutput(message)
            #self.hand.printCardListNames()
            self.chooseDiscard(1, self)
        # if the player has 2+ items (because they will always have 1 eternal item that cant be discarded)
        if self.items.getDeckLength() > 1:
            message = f"Player {self.num} had 1 treasure taken D:"
            Json.systemOutput(message)
            #self.items.printCardListNames()
            self.chooseDiscardTreasure(self)
        message = f"Player {self.num} exhausts all their energy :0"
        Json.systemOutput(message)
        itemsList = self.items.getCardList()
        for i in range(len(itemsList)):
            if isinstance(itemsList[i], GoldTreasure):
                itemsList[i].setTapped(True)
        self.getCharacter().setTapped(0)
        # set hp to 0
        self.setHp(0)
        # PLAYER-BOARD JSON
        # remove the player and attack roll from the stack (relevant if player dies to a bomb mid combat)
        stack = self.getRoom().getStack().getStack()
        if len(stack) == 0:
            return  # stack is empty so have this to avoid an error
        if isinstance(stack[0][0], DeclaredAttack):
            # remove combat from stack if the active player is the one who died
            if self == self.getRoom().getActivePlayer():
                stack.pop(0)
                # if the stack is empty
                if len(stack) == 0:
                    return
                # if there is still an attack roll/bomb on the stack
                stack.pop(0)
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
