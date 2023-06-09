# Contributions
#   Jackson Cashman:
#       All files
#   Ethan Sandoval:
#       checkResponse
"""
Everything is within a Room (Stack, Board, Players)
"""
import time
import json
import sys
from Coins import CoinStack
from LootCards import *
from Board import *
from SilverTreasureCards import TakeDamageTreasure
from SilverTreasureCards import DiceEffectTreasure
from JsonOutputHelper import JsonOutputHelper

Json = JsonOutputHelper()


class Room:
    def __init__(self, stack, board):
        self.stack = stack
        self.players = []
        self.board = board
        # activePlayerIndex is the player who's turn it is currently (P1 is 0)
        self.activePlayerIndex = -1

    # getters
    def getPlayersJsonObject(self):
        if len(self.players) == 0:
            playersListJsonObject = {"players": ["no players"]}
        else:
            playersJsonObjects = []
            for i in range(len(self.players)):
                playersJsonObjects.append(self.players[i].getJsonObject())
            playersListJsonObject = {"players": playersJsonObjects}
        return playersListJsonObject

    def getJsonObject(self):
        playersObject = self.getPlayersJsonObject()
        roomJsonObject = {
            "theStack": self.stack.getJsonObject(),
            "playersList": playersObject,
            "board": self.board.getJsonObject(),
            "activePlayerIndex": self.activePlayerIndex,
        }
        return roomJsonObject

    def getPlayers(self):
        return self.players

    def getStack(self):
        return self.stack

    def getBoard(self):
        return self.board

    def getActivePlayerIndex(self):
        return self.activePlayerIndex

    def getActivePlayer(self):
        return self.players[self.activePlayerIndex]

    def getPlayerAmount(self):
        return len(self.players)

    # other functions

    # the most recent player is always added at the end of the list
    def addPlayer(self, player):
        self.players.append(player)
        return

    def incrementActivePlayer(self):
        self.activePlayerIndex = (self.activePlayerIndex + 1) % len(self.players)
        return

    # reaction system
    # TODO: it would probably be nice for this to not be case sensitive
    def checkResponse(self, playerIndex):
        anyYes = False
        message = f"Player {self.players[playerIndex].getNumber()}, do you want to respond to {self.getStack().getStack()[-1][0].getName()}"
        Json.choiceOutput(
            self.players[playerIndex].getSocketId(), message, ["Yes", "No"]
        )
        inp1 = int(input())
        if inp1 == 1:
            message = "Do you want to play a loot card from your hand or play an active treasure"
            Json.choiceOutput(
                self.players[playerIndex].getSocketId(),
                message,
                ["Loot Card", "Treasure Card", "Cancel"],
            )
            inp2 = int(input())
            if inp2 == 1:
                if self.players[playerIndex].getTapped() < 1:
                    message = "You can't play any more loot cards this turn."
                    Json.systemPrivateOutput(
                        self.players[playerIndex].getSocketId(), message
                    )
                else:
                    anyYes = True
                    lootPlay(self.players[playerIndex])
            elif inp2 == 2:
                anyYes = True
                itemPlay(self.players[playerIndex])
            else:  # CANCEL
                return anyYes
        return anyYes

    def addToStack(self, obj):
        self.stack.add(obj)
        # check if anyone wants to play another card that would be resolved before the previous one
        playerList = obj[1].getRoom().getPlayers()
        response = False  # this var prevents anyone from responding to something that has already been responded to when set to true
        for i in range(len(playerList)):
            nextPlayerIndex = (self.activePlayerIndex + i) % len(playerList)
            if (len(self.stack.getStack()) > 0) and (response == False):
                response = self.checkResponse(nextPlayerIndex)
        return

    def useTopStack(self, playerIndex):
        self.stack.useTop(self)
        # Print specific player information, as well as board info for frontend rendering.
        playerList = self.players

        # for player in playerList:
        #     print(player.getPlayerHandObject())
        # print("USE TOP STACK" + self.stack.getLastResolved()[0].getName())

        response = False  # this var prevents anyone from responding to something that has already been responded to when set to true
        if len(self.stack.getStack()) == 0:
            return
        # TODO: need to add another or for death effects
        if isinstance(self.stack.getStack()[0][0], DeclaredAttack) and (
            isinstance(self.stack.getLastResolved()[0], Dice)
            or isinstance(self.stack.getLastResolved()[0], TakeDamageTreasure)
            or isinstance(self.stack.getLastResolved()[0], DiceEffectTreasure)
        ):
            # return early to prevent a prompted response for a declared attack after it has already been added to the stack
            return
        # check for responses here
        for i in range(len(playerList)):
            nextPlayerIndex = (self.activePlayerIndex + i) % len(playerList)
            if (len(self.stack.getStack()) > 0) and (response == False):
                response = self.checkResponse(nextPlayerIndex)
        return

    # this function is used to use the TakeDamageTreasures use function, we need this because of damageNum is needed in
    # use function for TakeDamageTreasures
    def useDamageEffect(self, playerIndex, damageNum):
        # this takes the TakeDamageTreasure off the stack
        self.stack.setLastResolved(self.stack.getStack().pop(-1))
        # this uses the TakeDamageTreasure card
        self.stack.getLastResolved()[0].use(self.stack.getLastResolved()[1], damageNum)
        playerList = self.players
        for player in playerList:
            Json.playerHandOutput(player)
            Json.playerBoardOutput(player)
        response = False  # this var prevents anyone from responding to something that has already been responded to when set to true
        if len(self.stack.getStack()) == 0:
            return
        # TODO: need to add another or for death effects
        if isinstance(self.stack.getStack()[0][0], DeclaredAttack) and (
            isinstance(self.stack.getLastResolved()[0], Dice)
            or isinstance(self.stack.getLastResolved()[0], TakeDamageTreasure)
            or isinstance(self.stack.getLastResolved()[0], DiceEffectTreasure)
        ):
            # return early to prevent a prompted response for a declared attack after it has already been added to the stack
            return
        # check for responses here
        for i in range(len(playerList)):
            nextPlayerIndex = (self.activePlayerIndex + i) % len(playerList)
            if (len(self.stack.getStack()) > 0) and (response == False):
                response = self.checkResponse(nextPlayerIndex)
        return

    def displayEntities(self):
        # entities = []
        # for i in range(len(self.players)):
        #    entities.append(self.players[i].getCharacter())
        # for i in range(self.board.getMaxMonsterSlots()):
        #    entities.append(self.board.getMonster(i + 1))
        # for i in range(len(entities)):
        #    print(f"{i + 1}: {entities[i].getName()}")
        return

    def displayCharacters(self):
        # for i in range(len(self.players)):
        #    character = self.players[i].getCharacter()
        #    print(f"{i + 1}: {character.getName()}\n  HP: {character.getHp()}\n  Coins: {self.players[i].getCoins()}"
        #          f"\n  Items: {len(self.players[i].getItems().getCardList())}\n  Souls: {self.players[i].getSouls()}\n")
        return

    def getEntity(self, index):
        entities = []
        for i in range(len(self.players)):
            entities.append(self.players[i].getCharacter())
        for i in range(self.board.getMaxMonsterSlots()):
            entities.append(self.board.getMonster(i + 1))
        return entities[index - 1]

    def getEntities(self):
        entities = []
        for i in range(len(self.players)):
            entities.append(self.players[i].getCharacter())
        for i in range(self.board.getMaxMonsterSlots()):
            entities.append(
                self.board.getMonster(i + 1)
            )  # did +1 because getMonster already -1,
            # but we need to start at 0 not -1
        return entities

    def printBoardSection(self):
        for player in self.players:
            print(json.dumps(player.getPlayerBoardSectionObject()))
            # time.sleep(1)
            sys.stdout.flush()
