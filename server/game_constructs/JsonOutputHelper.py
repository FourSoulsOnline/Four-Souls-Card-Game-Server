# Developer: Daniel De Guzman
# JsonOutputHelper prints JSON objects with a message flag.

import sys
import json
import time
class JsonOutputHelper:
    # Timer Value to let gameserver.js parse the message.
    timer = 1
    def __init__(self):
        pass

    # Print the json message, flush stdout, and sleep.
    def printOutput(self, jsonMessage):
        print(json.dumps(jsonMessage))
        sys.stdout.flush()
        time.sleep(self.timer)
    
    # Handle choices message, where choices is array of strings.
    def choiceOutput(self, playerSocket, choiceMessage, choices):
        # choices should always be an array of strings
        choiceMessage = {
            "messageFlag": "CHOICE",
            "socketID": playerSocket,
            "choiceMessage": choiceMessage,
            "choices": choices
        }
        self.printOutput(choiceMessage)

    # Handle system output.
    def systemOutput(self, message):
        systemMessage = {
            "messageFlag": "SYSTEM",
            "systemMessage": message
        }
        self.printOutput(systemMessage)

    # Handle a system output to a specific Player
    def systemPrivateOutput(self, socketId, message):
        systemPrivateMessage = {
            "messageFlag": "SYSTEM-PRIVATE",
            "socketID": socketId,
            "systemMessage": message
        }
        self.printOutput(systemPrivateMessage)

    # Handle player hand output, where handJsonObjects is the list of cards in a player's hand.
    def playerHandOutput(self, socketId, handJsonObjects):
        playerObject = {
            "messageFlag": "PLAYER-HAND",
            "socketID": socketId,
            "hand": handJsonObjects
        }
        self.printOutput(playerObject)

    # Handle the Player Board output section. NOTE: need to update itemsJsonObject
    def playerBoardOutput(self, playerNumber, character, cardCount, coins, souls, itemsJsonObject):
        playerObject = {
            "messageFlag": "PLAYER-BOARD",
            "playerNumber": playerNumber,
            "character": character,
            "cardCount": cardCount,
            "coins": coins,
            "souls": souls,
            "items": itemsJsonObject
        }
        self.printOutput(playerObject)

    # Handle the treasure section output
    def treasureOutput(self, treasures):
        treasureOutput = {
            "messageFlag": "TREASURE",
            "treasures": treasures
        }
        self.printOutput(treasureOutput)

    # Handle the Dice output
    def diceOutput(self, result):
        diceObject = {
            "messageFlag": "DICE",
            "result": result
        }
        self.printOutput(diceObject)

    # Handle the monster section output
    def monsterOutput(self, monsters):
        monsterObject = {
            "messageFlag": "MONSTER",
            "monsters": monsters
        }
        self.printOutput(monsterObject)

    # Handle the Discard Loot Deck output
    def discardLootDeckOutput(self, discardLoot):
        discardObject = {
            "messageFlag": "DISCARD-LOOT",
            "cards": discardLoot
        }
        self.printOutput(discardObject)

    # Handle the DIscard Treasure Deck output
    def discardTreasureDeckOutput(self, discardTreasure):
        discardObject = {
            "messageFlag": "DISCARD-TREASURE",
            "cards": discardTreasure
        }
        self.printOutput(discardObject)

    # Handle the Discard Monster Deck output.
    def discardMonsterDeckOutput(self, discardMonster):
        discardObject = {
            "messageFlag": "DISCARD-MONSTER",
            "cards": discardMonster
        }
        self.printOutput(discardObject)

    def stackOutput(self, stackContent):
        stackContent = {
            "messageFlag": "STACK",
            "content": stackContent
        }
        self.printOutput(stackContent)