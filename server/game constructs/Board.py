# Contributions
#   Jackson Cashman:
#       __init__, checkMonsterSlots, displayActiveMonsters, discardActiveMonster, discardMonsterIndex, findMatchingMonster
#       lootPlay, startTurn, midTurn, endTurn, checkTreasureSlots, displayActiveTreasures, findMatchingTreasure
#   Ethan Sandoval:
#       __init__, checkMonsterSlots, addMonsterSlot, discardActiveMonster, discardActiveMonster, getMonster
#       itemPlay, addTreasureSlot, checkTreasureSlots, displayActiveTreasures
#   Daniel De Guzman:
#       getJsonObject()
'''
The Board Contains all Decks (including discard piles) and Monsters/Treasures in their deck slots
Board is an attribute of a Room
Board is accessible from a Player
'''
from Decks import Deck
from Cards import *
from Coins import *
from LootReward import *
from TreasureReward import TreasureReward
from DeclareAttack import DeclaredAttack
from DeclarePurchase import DeclaredPurchase
from SilverTreasureCards import PlainSilverTreasure
from SilverTreasureCards import StartTurnTreasure
from SilverTreasureCards import EndTurnTreasure
from Events import Event

def lootPlay(player):
    if player.getHand().getDeckLength() == 0:
        print("You have no loot cards in your hand!\n")
    else:
        player.getHand().printCardListNames()
        print(f"{player.getHand().getDeckLength() + 1}: Cancel\n")
        num = int(input("What loot card do you want to play?: "))
        print("")
        handLen = player.getHand().getDeckLength()
        # cancel the loot play
        if num > handLen:
            pass
        elif player.getTapped() < 1:
            print("You can't play another loot card this turn.\n")
        else:
            # remove the used card from hand
            loot = player.getHand().removeCardIndex(num - 1)
            # use the loot card
            player.addToStack(loot)
            player.getRoom().useTopStack(player.getNumber())
    return

def itemPlay(player):
    if player.getItems().getDeckLength() == 0:
        print("You have no treasure cards in your hand!\n")
    else:
        player.getItems().printCardListNames()
        print(f"{player.getItems().getDeckLength() + 1}: Cancel\n")
        num = int(input("What tresure card do you want to play?: "))
        print("")
        # cancel option
        if num > len(player.getItems().getCardList()):
            return
        treasure = player.getItems().getCardList()[num - 1]
        if treasure.getTapped() == True:
            print("That item can't be used again this turn.\n")
            return
        # use the treasure card
        player.addToStack(treasure)
        player.getRoom().useTopStack(player.getNumber())
    return

class Board:
    def __init__(self, monsterDeck, treasureDeck, lootDeck):
        # max----Slots is the number of slots for that card type on the board
        self.maxMonsterSlots = 20
        self.maxTreasureSlots = 20
        # active----- is the populated slots for that card type. it should always be a list of lists
        # (even if the inside lists only have a single element)
        self.activeMonsters = [[], []] # active monsters are stored on the -1 index
        self.activeTreasures = [[], []]
        # the deck of ----- cards
        self.monsterDeck = monsterDeck
        self.treasureDeck = treasureDeck
        self.lootDeck = lootDeck
        # discard piles for the appropriate decks
        self.discardLootDeck = Deck([])
        self.discardMonsterDeck = Deck([])
        self.discardTreasureDeck = Deck([])
        # effects that are on the board
        # each element in global effect is a list of [card object, the owner]
        # reduce damage does not go in globalEffects
        # TODO: when someone loses an item/steals an item make sure to update globalEffects
        self.globalEffects = []

    def getJsonObject(self):
        boardObject = {
            "maxMonsterSlotsNumber": self.maxMonsterSlots,
            "maxTreasureSlotsNumber": self.maxTreasureSlots,
            "activeMonsters": self.activeMonsters,
            "activeTreasures": self.activeTreasures,
            "monsterDeck": self.monsterDeck.getJsonObject(),
            "treasureDeck": self.treasureDeck.getJsonObject(),
            "lootDeck": self.lootDeck.getJsonObject(),
            "discardMonsterDeck": self.discardMonsterDeck.getJsonObject(),
            "discardTreasureDeck": self.discardTreasureDeck.getJsonObject(),
            "discardLootDeck": self.discardLootDeck.getJsonObject(),
            "globalEffects": self.globalEffects
        }
        return boardObject

    def getLootDeck(self):
        return self.lootDeck

    def getMonsterDeck(self):
        return self.monsterDeck

    def getTreasureDeck(self):
        return self.treasureDeck

    def getDiscardLootDeck(self):
        return self.discardLootDeck

    def getDiscardMonsterDeck(self):
        return self.discardMonsterDeck

    def getDiscardTreasureDeck(self):
        return self.discardTreasureDeck

    # returns the active monster in the specified slot
    def getMonster(self, slotNum):
        return self.activeMonsters[slotNum - 1][-1]

    # returns all monster slots
    def getMonsters(self):
        return self.activeMonsters

    # returns the Treasure in the specified slot
    def getTreasure(self, slotNum):
        return self.activeTreasures[slotNum - 1][-1]

    # returns all treasure slots
    def getTreasures(self):
        return self.activeTreasures

    def getMaxMonsterSlots(self):
        return self.maxMonsterSlots

    def getGlobalEffects(self):
        return self.globalEffects

    def startTurn(self, player):
        print(f"Player {player.getNumber()}'s Turn!\n")
        # recharge all items and character
        player.getCharacter().setTapped(2)
        player.getCharacter().setAttacksLeft(1)
        player.getCharacter().setPurchases(1)
        for i in range(player.getItems().getDeckLength()):
            if isinstance(player.getItems().getCardList()[i], GoldTreasure):
                player.getItems().getCardList()[i].setTapped(False)

        # check for "at start of your turn" effects in globalEffects
        for i in range(len(self.globalEffects)):
            if isinstance(self.globalEffects[i][0], StartTurnTreasure):
                # if it is the start of the itemUsers turn
                itemUser = self.globalEffects[i][1]
                if player.getNumber() == itemUser.getNumber():
                    itemUser.addToStack(self.globalEffects[i][0])
                    itemUser.getRoom().useTopStack(itemUser.getNumber())

        # active player loots
        # TODO: this should go on the stack
        player.loot(1)
        return self.midTurn(player)

    def midTurn(self, player):
        inp = 0
        # increment activePlayer in room
        player.getRoom().incrementActivePlayer()
        while inp != 6:
            # print player stats and ask them what they want to do
            print(f"Player {player.getNumber()}:\n  HP: {player.getHp()}\n  Attack: {player.getAttack()}"
                  f"\n  Coins: {player.getCoins()}\n  Loot Plays Remaining: {player.getTapped()}\n  Hand: {player.getHand().getDeckLength()}\n")
            print("What would you like to do?:\n1. Play a Loot Card\n2. Activate a Gold Treasure\n"
                  "3. Attack a Monster\n4. Purchase a Shop Item\n5. Show other Players\n6. End Turn")
            inp = int(input("  Choice: "))
            print("")
            if inp == 1:
                lootPlay(player)
            elif inp == 2:
                itemPlay(player)
            elif inp == 3:
                if player.getCharacter().getAttacksLeft() <= 0:
                    print("You aren't able to attack again this turn.\n")
                else:
                    # show active monsters and prompt an attack
                    self.displayActiveMonsters()
                    num = int(input("What monster do you want to attack?: "))
                    # cancel prompted attack
                    if num >= (len(self.activeMonsters) + 1):
                        pass
                    # add the declared attack to the stack
                    else:
                        player.addToStack(DeclaredAttack(self.getMonster(num)))
                        # clear anything at the top of the stack that isnt the DeclaredAttack
                        ''' # this commented version will make the game run but could make bugs harder to detect
                        try:
                            while isinstance(player.getRoom().getStack().getStack()[-1][0], DeclaredAttack) != True:
                                player.getRoom().getStack().useTop()
                            # use the declared attack
                            player.getRoom().getStack().useTop()
                        except: # monster killed with a bomb or similar during combat
                            # decrement the number of attacks user can initiate this turn
                            player.getCharacter().subtractAttacksLeft()
                            print("Combat ended without attack roll.")
                        '''
                        #'''
                        if len(player.getRoom().getStack().getStack()) > 0:
                            while isinstance(player.getRoom().getStack().getStack()[-1][0], DeclaredAttack) != True:
                                player.getRoom().getStack().useTop()
                            # use the declared attack
                            player.getRoom().getStack().useTop()
                        #'''
            elif inp == 4:
                if player.getCharacter().getPurchases() <= 0:
                    print("You aren't able to purchase again this turn.\n")
                elif player.getCoins() < 10:
                    print("You do not have enough coins to purchase an item.\n")
                else:
                    # show active treasures and prompt a purchase
                    self.displayActiveTreasures()
                    num = int(input("Which treasure would you like to purchase?: "))
                    # cancel prompted purchase on invalid input
                    if num >= (len(self.activeTreasures) + 1):
                        pass
                    # choose which treasure to buy
                    else:
                        player.addToStack(DeclaredPurchase(self.getTreasure(num)))
                        # clear anything at the top of the stack that isnt the DeclaredPurchase
                        while isinstance(player.getRoom().getStack().getStack()[-1][0], DeclaredPurchase) != True:
                            player.getRoom().getStack().useTop()
                        # use the declared attack
                        player.getRoom().getStack().useTop()
            elif inp == 5:
                player.getRoom().displayCharacters()
            else:
                if player.getCharacter().getMandatoryAttacks() < 1:
                    return self.endTurn(player)
                else:
                    print("You must attack another time this turn!\n")
                    inp = 0

    def endTurn(self, player):
        # check for "at end of your turn" effects in globalEffects
        for i in range(len(self.globalEffects)):
            if isinstance(self.globalEffects[i][0], EndTurnTreasure):
                # if it is the end of the itemUsers turn
                itemUser = self.globalEffects[i][1]
                if player.getNumber() == itemUser.getNumber():
                    itemUser.addToStack(self.globalEffects[i][0])
                    itemUser.getRoom().useTopStack(itemUser.getNumber())

        # reduce loot plays to 1 if above
        if player.getTapped() > 1:
            player.getCharacter().setTapped(1)
        players = player.getRoom().getPlayers()
        entities = player.getRoom().getEntities()
        # Resets the HP of all entities on the board
        for i in range(len(entities)):
            entities[i].setHp(entities[i].getMaxHp())
            entities[i].setAttack(entities[i].getMaxAttack())
        numPlayers = len(players)
        nextPlayer = (player.getNumber() + 1) % numPlayers
        return self.startTurn(players[nextPlayer - 1])

    # check each monster slot to look for any empty slots
    # if an empty slot is found, fill it with the top card of the monster deck
    # player is some player, not guaranteed to be the active player (necessary input for Events)
    def checkMonsterSlots(self, player):
        # fill new monster slots if there are less than the maximum slots
        if (len(self.activeMonsters)) < self.maxMonsterSlots:
            for i in range(self.maxMonsterSlots - (len(self.activeMonsters))):
                self.activeMonsters += [[]]
        # for every monster slot
        for i in range(len(self.activeMonsters)):
            # if the slot is empty, fill it with the top card of the monster deck
            if len(self.activeMonsters[i]) == 0:
                # TODO: this if statement should shuffle the deck instead
                if self.monsterDeck.getDeckLength() <= 0:
                    raise IndexError("Monster Deck is Empty")
                nextMonster = self.monsterDeck.deal()
                self.activeMonsters[i].append(nextMonster)
                # add event cards to the stack if drawn
                if isinstance(nextMonster, Event):
                    player.getRoom().addToStack([nextMonster, player.getRoom().getActivePlayer()])
                    player.getRoom().useTopStack(0)
        return

    def checkTreasureSlots(self):
        # fill new treasure slots if there are less than the maximum slots
        if (len(self.activeTreasures)) < self.maxTreasureSlots:
            for i in range(self.maxTreasureSlots - (len(self.activeTreasures))):
                self.activeTreasures += [[]]
        for i in range(len(self.activeTreasures)):
            # if the slot is empty, fill it with the top card of the treasure deck
            if len(self.activeTreasures[i]) == 0:
                # TODO: this if statement should shuffle the deck instead
                if self.treasureDeck.getDeckLength() <= 0:
                    raise IndexError("Treasure Deck is Empty")
                self.activeTreasures[i].append(self.treasureDeck.deal())
        return

    def addMonsterSlot(self):
        self.maxMonsterSlots += 1
        return

    def addTreasureSlot(self):
        self.maxTreasureSlots += 1
        return

    def coveringMonster(self):
        # TODO:add a monster on top of the monster card on the list
        pass

    # prints the name of each active monster
    def displayActiveMonsters(self):
        print("Here are the monsters on the Board:")
        for i in range(len(self.activeMonsters)):
            if len(self.activeMonsters[i]) == 0:
                print("Empty")
            # print the name of the -1'th index of each monster slot
            else:
                print(f'{i + 1}: {self.activeMonsters[i][-1].getName()}')
                print(f'  HP: {self.activeMonsters[i][-1].getHp()}')
                print(f'  Dice: {self.activeMonsters[i][-1].getDiceValue()}')
                print(f'  Attack: {self.activeMonsters[i][-1].getAttack()}')
                # get the rewards of the monster into a string to display
                rewardString = ""
                for j in range(len(self.activeMonsters[i][-1].getReward())):
                    if isinstance(self.activeMonsters[i][-1].getReward()[j], CoinStack):
                        rewardString = rewardString + "    Coins: " + str(self.activeMonsters[i][-1].getReward()[j].getCount()) + "\n"
                    elif isinstance(self.activeMonsters[i][-1].getReward()[j], LootReward):
                        rewardString = rewardString + "    Loot: " + str(self.activeMonsters[i][-1].getReward()[j].getCount()) + "\n"
                    elif isinstance(self.activeMonsters[i][-1].getReward()[j], TreasureReward):
                        rewardString = rewardString + "    Treasure: " + str(self.activeMonsters[i][-1].getReward()[j].getCount()) + "\n"
                    elif isinstance(self.activeMonsters[i][-1].getReward()[j], LootXReward):
                        rewardString = rewardString + "    Loot: X" + "\n"
                    elif isinstance(self.activeMonsters[i][-1].getReward()[j], CoinXReward):
                        rewardString = rewardString + "    Coins: X" + "\n"
                print(f'  Reward(s): \n{rewardString}')
        print(f"{len(self.activeMonsters) + 1}: CANCEL\n")
        return

    def displayActiveTreasures(self):
        print("Here are the treasures in the Shop (10 cents):")
        for i in range(len(self.activeTreasures)):
            if len(self.activeTreasures[i]) == 0:
                print("Empty")
            else:
                print(f'{i + 1}: {self.activeTreasures[i][-1].getName()}\n')
        print(f"{len(self.activeTreasures) + 1}: CANCEL\n")
        return

    def discardLoot(self, player, handIndex):
        discard = player.getHand().removeCardIndex(handIndex)
        self.discardLootDeck.addCardTop(discard)
        return

    # a special case will need to be added for Sack of Pennies and The Poop
    # because they are gold treasures with passive effects
    def discardTreasure(self, player, itemIndex):
        discard = player.getItems().getCard(itemIndex)
        # if the card being discarded has a global effect
        plainSilver = isinstance(player.getItems().getCardList()[itemIndex], PlainSilverTreasure)
        plainGold = isinstance(player.getItems().getCardList()[itemIndex], GoldTreasure)
        if (plainSilver is False) and (plainGold is False):
            # remove that global effect from the list
            for i in range(len(self.globalEffects)):
                if self.globalEffects[i][0] == discard:
                    self.globalEffects.remove(self.globalEffects[i])
                    break
        player.getItems().removeCardIndex(itemIndex)
        self.discardTreasureDeck.addCardTop(discard)
        return

    # this function asks the player for input on what monster to discard
    def discardActiveMonster(self):
        self.displayActiveMonsters()
        index = int(input("Which monster do you want to get rid of: "))
        index -= 1
        discard = (self.activeMonsters[index]).pop(-1)
        self.discardMonsterDeck.addCardTop(discard)
        return

    # this function discards a monster in the matching index passed in as a parameter
    def discardMonsterIndex(self, index):
        discard = (self.activeMonsters[index]).pop(-1)
        self.discardMonsterDeck.addCardTop(discard)
        return

    # clears a treasure in the matching index (used when a player purchases an item)
    def clearTreasureSlot(self, slotNum):
        (self.activeTreasures[slotNum-1]).pop()
        return

    # returns the index of a monster with the provided name
    def findMatchingMonster(self, name):
        for i in range(len(self.activeMonsters)):
            if self.activeMonsters[i][-1].getName() == name:
                return i

    # returns the index of a treasure with the provided name
    def findMatchingTreasure(self, name):
        for i in range(len(self.activeTreasures)):
            if self.activeTreasures[i][-1].getName() == name:
                return i

    # used to display a single monster, kinda not working correctly (testing with input 0-2), don't know if needed
    def displayMonster(self, index):
        print(self.activeMonsters[index - 1][-1].getName())
