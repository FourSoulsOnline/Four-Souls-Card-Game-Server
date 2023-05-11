# Contributions
#   Jackson Cashman:
#       __init__, checkMonsterSlots, displayActiveMonsters, discardMonsterIndex, findMatchingMonster
#       lootPlay, startTurn, midTurn, endTurn, checkTreasureSlots, displayActiveTreasures, findMatchingTreasure
#       checkGuppy, checkGuppySoul
#   Ethan Sandoval:
#       __init__, checkMonsterSlots, addMonsterSlot, getMonster, startTurn, midTurn, endTurn, forcedEndTurn,
#       itemPlay, addTreasureSlot, checkTreasureSlots, displayActiveTreasures, Timer system, stealTreasure,
#       displayMonster
#   Daniel De Guzman:
#       getJsonObject()
"""
The Board Contains all Decks (including discard piles) and Monsters/Treasures in their deck slots
Board is an attribute of a Room
Board is accessible from a Player
"""
from Decks import Deck
from Cards import *
from Coins import *
from LootReward import *
from TreasureReward import TreasureReward
from DeclareAttack import DeclaredAttack
from DeclarePurchase import DeclaredPurchase
from DeclarePurchase import DeclaredPurchaseMystery
from SilverTreasureCards import PlainSilverTreasure
from SilverTreasureCards import StartTurnTreasure
from SilverTreasureCards import EndTurnTreasure
from Events import Event
from JsonOutputHelper import JsonOutputHelper

Json = JsonOutputHelper()
import time
import threading
from threading import Timer

Json = JsonOutputHelper()


def forcedEndTurn(player):
    print("\ntime expired, ending turn...")
    return player.getBoard().endTurn(player)


def lootPlay(player):
    if player.getHand().getDeckLength() == 0:
        message = "You have no loot cards in your hand!"
        playerId = player.getSocketId()
        Json.systemPrivateOutput(playerId, message)
    else:
        # player.getHand().printCardListNames() #TODO: Comment this line in final version
        # print(f"{player.getHand().getDeckLength() + 1}: Cancel\n") #TODO: this line too
        num = player.chooseLootIndex() + 1
        handLen = player.getHand().getDeckLength()
        # cancel the loot play
        if num > handLen:
            pass
        elif player.getTapped() < 1:
            message = "You can't play another loot card this turn."
            playerId = player.getSocketId()
            Json.systemPrivateOutput(playerId, message)
        else:
            # remove the used card from hand
            loot = player.getHand().removeCardIndex(num - 1)
            # Message to update other players that someone is trying to play a card
            message = (
                f"Hey! Player {player.getNumber()} is trying to play {loot.getName()}"
            )
            Json.systemOutput(message)
            # use the loot card
            player.addToStack(loot)
            player.getRoom().useTopStack(player.getNumber())
            # check that it is a loot card that is discarded when used
            if loot.getName() != "Lost Soul":
                player.getBoard().getDiscardLootDeck().addCardTop(loot)
                Json.discardLootDeckOutput(player.getBoard().getDiscardLootDeck())
    return


def itemPlay(player):
    if player.getItems().getDeckLength() == 0:
        message = "You have no treasure cards in your hand!"
        playerId = player.getSocketId()
        Json.systemPrivateOutput(playerId, message)
    else:
        # player.getItems().printCardListNames() # TODO: comment this
        # print(f"{player.getItems().getDeckLength() + 1}: Cancel\n") # TODO: comment this
        num = player.chooseTreasureIndex() + 1
        # cancel option
        if num > len(player.getItems().getCardList()):
            return
        treasure = player.getItems().getCardList()[num - 1]
        # check to see if they choose a silver treasure card
        if isinstance(treasure, SilverTreasure):
            message = "Can't choose a card with a passive effect."
            playerId = player.getSocketId()
            Json.systemPrivateOutput(playerId, message)
            return
        # check to see if the card is tapped so it can't be used
        elif treasure.getTapped() == True:
            message = "That item can't be used again this turn."
            playerId = player.getSocketId()
            Json.systemPrivateOutput(playerId, message)
            return
        # Message to update other players that someone is trying to play a card
        message = (
            f"Hey! Player {player.getNumber()} is trying to play {treasure.getName()}"
        )
        Json.systemOutput(message)
        # use the treasure card
        player.addToStack(treasure)
        player.getRoom().useTopStack(player.getNumber())
    return


# returns True if a specified item is a Guppy item
def checkGuppy(item):
    name = item.getName()
    if "Guppy" in name:
        return True
    if name == "Dead Cat":
        return True


# TODO: users are given soul of guppy when having only 1 guppy item
# gives the player soul of guppy if applicable
def checkGuppySoul(treasureCard, player):
    # check for guppy
    if checkGuppy(treasureCard) is True:
        # check if they own a second guppy item
        items = player.getItems().getCardList()
        for i in range(player.getItems().getDeckLength()):
            if checkGuppy(items[i]) is True:
                # award soul of guppy
                player.getBoard().getSoulDict()["Guppy"] = True
                message = f"Player {player.getNumber()} achieved the Soul of Guppy!"
                Json.systemOutput(message)
                player.addSouls(1)
                Json.playerBoardOutput(player)
                return
    return


class Board:
    def __init__(self, monsterDeck, treasureDeck, lootDeck):
        # max----Slots is the number of slots for that card type on the board
        self.maxMonsterSlots = 10
        self.maxTreasureSlots = 20
        # active----- is the populated slots for that card type. it should always be a list of lists
        # (even if the inside lists only have a single element)
        self.activeMonsters = [[], []]  # active monsters are stored on the -1 index
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
        self.globalEffects = []
        # dictionary to keep track of which souls have been achieved
        # False --> not achieved, True --> achieved
        self.soulDict = {"Gluttony": False, "Greed": False, "Guppy": False}

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
            "globalEffects": self.globalEffects,
            "soulDict": self.soulDict,
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
        if slotNum <= self.maxTreasureSlots:
            return self.activeTreasures[slotNum - 1][-1]
        else:
            return self.treasureDeck.getCard(0)

    # returns all treasure slots
    def getTreasures(self):
        return self.activeTreasures

    def getMaxMonsterSlots(self):
        return self.maxMonsterSlots

    def getGlobalEffects(self):
        return self.globalEffects

    def getSoulDict(self):
        return self.soulDict

    def startTurn(self, player):
        Json.systemOutput(f"({player.getNumber()}) {player.getUsername()}'s Turn!")
        # recharge all items and character
        player.getCharacter().setTapped(2)
        player.getCharacter().setAttacksLeft(1)
        player.getCharacter().setPurchases(1)
        for i in range(player.getItems().getDeckLength()):  # recharge items
            if isinstance(player.getItems().getCardList()[i], GoldTreasure):
                player.getItems().getCardList()[i].setTapped(False)
        # update what tools the player has accessible before using "start of turn" treasures
        Json.playerBoardOutput(player)

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
        Json.playerBoardOutput(player)
        Json.playerHandOutput(player)
        # Output activeMonsters to get updated health/atk
        Json.monsterOutput(self.activeMonsters)
        # Update hp/other stats of players
        for i in range(len(player.getRoom().getPlayers())):
            Json.playerBoardOutput(player.getRoom().getPlayers()[i])
        # time.sleep(1)
        while inp != 6:
            # at the start of each action, create a timer
            # timer = Timer(5.0, forcedEndTurn, kwargs={"player": player})
            # timer.start()

            """
            # trying to debug Timers
            # get a list of all active threads
            thread_list = threading.enumerate()

            # iterate over the list and print out information about each thread
            for thread in thread_list:
                print("Thread name:", thread.getName())
                print("Thread ID:", thread.ident)
                print("Thread is daemon:", thread.daemon)
            """

            choices = [
                "Play a Loot Card",
                "Activate a Gold Treasure",
                "Attack a Monster",
                "Purchase a Shop Item",
                "Trade",
                "End Turn",
            ]
            Json.choiceOutput(
                player.getSocketId(),
                "It's your turn! What would you like to do?",
                choices,
            )
            inp = int(input())
            if inp == 1:
                # timer.cancel()
                lootPlay(player)
            elif inp == 2:
                # timer.cancel()
                itemPlay(player)
            elif inp == 3:
                if player.getCharacter().getAttacksLeft() <= 0:
                    message = f"You aren't able to attack again this turn."
                    Json.systemOutput(message)
                else:
                    # show active monsters and prompt an attack
                    # self.displayActiveMonsters() #TODO: Comment this and prints out
                    # print(f"{len(self.activeMonsters) + 1}: FACE DOWN MONSTER")
                    # print(f"{len(self.activeMonsters) + 2}: CANCEL\n")
                    message = f"What monster do you want to attack?"
                    monsterChoice = player.chooseAttackTarget(message)
                    # cover an existing monster
                    if monsterChoice == "face down monster":
                        # timer.cancel()
                        slotNum = self.coverMonster()
                        monsterChoice = self.activeMonsters[slotNum - 1][-1]
                    # cancel prompted attack
                    if monsterChoice == "cancel":
                        pass
                    # add the declared attack to the stack
                    else:
                        # timer.cancel()
                        player.addToStack(DeclaredAttack(monsterChoice))
                        # clear anything at the top of the stack that isnt the DeclaredAttack
                        if len(player.getRoom().getStack().getStack()) > 0:
                            while (
                                isinstance(
                                    player.getRoom().getStack().getStack()[-1][0],
                                    DeclaredAttack,
                                )
                                != True
                            ):
                                player.getRoom().getStack().useTop(player.getRoom())
                            # use the declared attack
                            player.getRoom().getStack().useTop(player.getRoom())
            elif inp == 4:
                if player.getCharacter().getPurchases() <= 0:
                    message = f"You aren't able to purchase again this turn."
                    Json.systemOutput(message)
                elif player.getCoins() < 10:
                    message = f"You do not have enough coins to purchase an item."
                    Json.systemOutput(message)
                else:
                    # show active treasures and prompt a purchase
                    # self.displayActiveTreasures() #TODO: comment this and prints out
                    # print(f"{len(self.activeTreasures) + 1}: FACE DOWN TREASURE")
                    # print(f"{len(self.activeTreasures) + 2}: CANCEL\n")
                    message = f"Which treasure would you like to purchase?"
                    treasureChoice = player.choosePurchaseTarget(message)
                    # cancel prompted purchase on invalid input
                    if treasureChoice == "cancel":
                        pass
                    # choose which treasure to buy
                    else:
                        # purchase face down treasure
                        if treasureChoice == "face down treasure":
                            # timer.cancel()
                            treasureChoice = self.treasureDeck.deal()
                            player.addToStack(DeclaredPurchaseMystery(treasureChoice))
                        # purchase a treasure from treasure slot
                        else:
                            # timer.cancel()
                            player.addToStack(DeclaredPurchase(treasureChoice))

                        # clear anything at the top of the stack that isnt the DeclaredPurchase
                        while (
                            isinstance(
                                player.getRoom().getStack().getStack()[-1][0],
                                DeclaredPurchase,
                            )
                            != True
                        ) and (
                            isinstance(
                                player.getRoom().getStack().getStack()[-1][0],
                                DeclaredPurchaseMystery,
                            )
                            != True
                        ):
                            player.getRoom().getStack().useTop(player.getRoom())
                        # use the declared attack
                        player.getRoom().getStack().useTop(player.getRoom())
            # Trading option
            elif inp == 5:
                # timer.cancel()
                message = f"Do you want to give or receive?"
                Json.choiceOutput(
                    player.getSocketId(), message, ["Give", "Receive", "Cancel"]
                )
                choice = int(input())
                if choice == 1:
                    message = f"Choose a player."
                    chosenPlayer = player.getChosenPlayer(message, player)
                    valueList = []
                    for i in range(player.getCoins()):
                        valueList.append(str(i + 1))
                    message = "How much do you want to give?"
                    Json.choiceOutput(player.getSocketId(), message, valueList)
                    amount = int(input())
                    player.subtractCoins(amount)
                    chosenPlayer.addCoins(amount)
                    message = f"Player {player.getNumber()} gave {amount} coin(s) to Player {chosenPlayer.getNumber()}."
                    Json.systemOutput(message)
                elif choice == 2:
                    playerList = player.getRoom().getPlayers()
                    for i in range(len(playerList) - 1):
                        nextPlayerIndex = (
                            player.getRoom().getActivePlayerIndex() + i + 1
                        ) % len(playerList)
                        message = f"Player {nextPlayerIndex + 1}: How much do you want to give"
                        valueList = []
                        for i in range(playerList[nextPlayerIndex].getCoins()):
                            valueList.append(str(i + 1))
                        valueList.append("None")
                        Json.choiceOutput(
                            playerList[nextPlayerIndex].getSocketId(),
                            message,
                            valueList,
                        )
                        amount = int(input())
                        if playerList[nextPlayerIndex].getCoins() < amount:
                            message = "Choose to not give any"
                            Json.systemOutput(message)
                        else:
                            playerList[nextPlayerIndex].subtractCoins(amount)
                            player.addCoins(amount)
                            message = f"Player {nextPlayerIndex + 1} gave {amount} coin(s) to Player {player.getNumber()}"
                            Json.systemOutput(message)
                else:
                    pass
            elif inp == 6:
                if player.getCharacter().getMandatoryAttacks() < 1:
                    # timer.cancel()
                    return self.endTurn(player)
                else:
                    message = "You must attack another time this turn!"
                    playerId = player.getSocketId()
                    Json.systemPrivateOutput(playerId, message)
                    inp = 0
            else:
                player.getRoom().displayCharacters()

    def endTurn(self, player):
        # check for "at end of your turn" effects in globalEffects
        for i in range(len(self.globalEffects)):
            if (i + 1) > len(self.globalEffects):
                pass
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
                    # We want to show the Event Card before popping it off of the monster section.
                    Json.monsterOutput(self.activeMonsters)
                    player.getRoom().addToStack(
                        [nextMonster, player.getRoom().getActivePlayer()]
                    )
                    player.getRoom().useTopStack(0)
                    # is it possible that we may miss a monster slot here? ^ - D.D.
        # After filling all the spots, construct the Monster Array - D.D.
        Json.monsterOutput(self.activeMonsters)
        return

    # called at turn 0. fill slots and add revealed events to the bottom of the deck
    def checkMonsterSlotsTurnZero(self):
        # fill new monster slots if there are less than the maximum slots
        if (len(self.activeMonsters)) < self.maxMonsterSlots:
            for i in range(self.maxMonsterSlots - (len(self.activeMonsters))):
                self.activeMonsters += [[]]
        # for every monster slot
        for i in range(len(self.activeMonsters)):
            # if the slot is empty, fill it with the top card of the monster deck
            # replace event cards revealed this way
            while len(self.activeMonsters[i]) == 0:
                # TODO: this if statement should shuffle the deck instead
                if self.monsterDeck.getDeckLength() <= 0:
                    raise IndexError("Monster Deck is Empty")
                nextMonster = self.monsterDeck.deal()
                if isinstance(nextMonster, Event):
                    # put the event card on the bottom of the deck
                    self.monsterDeck.addCardBottom(nextMonster)
                else:
                    # put the non-event card in the active slot
                    self.activeMonsters[i].append(nextMonster)
        Json.monsterOutput(self.activeMonsters)
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
        Json.treasureOutput(self.activeTreasures)
        return

    def addMonsterSlot(self):
        self.maxMonsterSlots += 1
        return

    def addTreasureSlot(self):
        self.maxTreasureSlots += 1
        return

    # TODO: monster passive effects should be removed while covered (might not get to this as there are no passive effects rn)
    # return the slot that the monster covers
    def coverMonster(self):
        topMonster = self.monsterDeck.deal()
        message = f"The face down monster is revealed to be {topMonster.getName()}!"
        Json.systemOutput(message)
        slotNum = int(input("Which slot would you like to cover?: "))
        self.activeMonsters[slotNum - 1].append(topMonster)
        Json.monsterOutput(self.activeMonsters)
        return slotNum

    # prints the name of each active monster
    def displayActiveMonsters(self):
        # print("Here are the monsters on the Board:")
        # for i in range(len(self.activeMonsters)):
        #    if len(self.activeMonsters[i]) == 0:
        #        print("Empty")
        #    # print the name of the -1'th index of each monster slot
        #    else:
        #        print(f'{i + 1}: {self.activeMonsters[i][-1].getName()}')
        #        print(f'  HP: {self.activeMonsters[i][-1].getHp()}')
        #        print(f'  Dice: {self.activeMonsters[i][-1].getDiceValue()}')
        #        print(f'  Attack: {self.activeMonsters[i][-1].getAttack()}')
        #        # get the rewards of the monster into a string to display
        #        rewardString = ""
        #        for j in range(len(self.activeMonsters[i][-1].getReward())):
        #            if isinstance(self.activeMonsters[i][-1].getReward()[j], CoinStack):
        #                rewardString = rewardString + "    Coins: " + str(self.activeMonsters[i][-1].getReward()[j].getCount()) + "\n"
        #            elif isinstance(self.activeMonsters[i][-1].getReward()[j], LootReward):
        #                rewardString = rewardString + "    Loot: " + str(self.activeMonsters[i][-1].getReward()[j].getCount()) + "\n"
        #            elif isinstance(self.activeMonsters[i][-1].getReward()[j], TreasureReward):
        #                rewardString = rewardString + "    Treasure: " + str(self.activeMonsters[i][-1].getReward()[j].getCount()) + "\n"
        #            elif isinstance(self.activeMonsters[i][-1].getReward()[j], LootXReward):
        #                rewardString = rewardString + "    Loot: X" + "\n"
        #            elif isinstance(self.activeMonsters[i][-1].getReward()[j], CoinXReward):
        #                rewardString = rewardString + "    Coins: X" + "\n"
        #        print(f'  Reward(s): \n{rewardString}')
        return

    def displayActiveTreasures(self):
        # print("Here are the treasures in the Shop (10 cents):")
        # for i in range(len(self.activeTreasures)):
        #    if len(self.activeTreasures[i]) == 0:
        #        print("Empty")
        #    else:
        #        print(f'{i + 1}: {self.activeTreasures[i][-1].getName()}\n')
        return

    def discardLoot(self, player, handIndex):
        discard = player.getHand().removeCardIndex(handIndex)
        self.discardLootDeck.addCardTop(discard)
        Json.playerHandOutput(player)
        Json.discardLootDeckOutput(self.discardLootDeck)
        return

    # a special case will need to be added for Sack of Pennies and The Poop
    # because they are gold treasures with passive effects
    def discardTreasure(self, player, itemIndex):
        discard = player.getItems().getCard(itemIndex)
        # if the card being discarded has a global effect
        plainSilver = isinstance(
            player.getItems().getCardList()[itemIndex], PlainSilverTreasure
        )
        plainGold = isinstance(player.getItems().getCardList()[itemIndex], GoldTreasure)
        if (plainSilver is False) and (plainGold is False):
            # remove that global effect from the list
            for i in range(len(self.globalEffects)):
                if self.globalEffects[i][0] == discard:
                    self.globalEffects.remove(self.globalEffects[i])
                    break
        player.getItems().removeCardIndex(itemIndex)
        self.discardTreasureDeck.addCardTop(discard)
        Json.playerBoardOutput(player)
        Json.discardTreasureDeckOutput(self.discardTreasureDeck)
        return

    # this function discards a monster in the matching index passed in as a parameter
    def discardMonsterIndex(self, index):
        discard = (self.activeMonsters[index]).pop(-1)
        self.discardMonsterDeck.addCardTop(discard)
        Json.monsterOutput(self.activeMonsters)
        Json.discardMonsterDeckOutput(self.discardMonsterDeck)
        return

    # clears a treasure in the matching index (used when a player purchases an item)
    def clearTreasureSlot(self, slotNum):
        (self.activeTreasures[slotNum - 1]).pop()
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
        # print(self.activeMonsters[index - 1][-1].getName())
        return

    # used to steal cards from another player, user will steal card from chosenPlayer4
    def stealTreasure(self, user, chosenPlayer, cardIndex):
        # user is person stealing the card from chosenPlayer, cardIndex is card wanting to steal
        discard = chosenPlayer.getItems().getCard(cardIndex)
        plainSilver = isinstance(
            chosenPlayer.getItems().getCard(cardIndex), PlainSilverTreasure
        )
        plainGold = isinstance(chosenPlayer.getItems().getCard(cardIndex), GoldTreasure)
        # check to see if item would be in global effects, if so update global effects
        if (plainSilver is False) and (plainGold is False):
            # update global effects so the user is now the owner of the item
            for i in range(len(self.globalEffects)):
                if self.globalEffects[i][0] == discard:
                    self.globalEffects[i][1] = user
                    break
        # delete the stolen card from chosenPlayer
        chosenPlayer.getItems().removeCardIndex(cardIndex)
        # add the card to user's items
        checkGuppySoul(discard, user)
        user.getItems().addCardBottom(discard)
        return
