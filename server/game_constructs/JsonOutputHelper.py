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
            "choices": choices,
        }
        self.printOutput(choiceMessage)

    # Handle system output.
    def systemOutput(self, message):
        systemMessage = {"messageFlag": "SYSTEM", "systemMessage": message}
        self.printOutput(systemMessage)

    # Handle a system output to a specific Player
    def systemPrivateOutput(self, socketId, message):
        systemPrivateMessage = {
            "messageFlag": "SYSTEM-PRIVATE",
            "socketID": socketId,
            "systemMessage": message,
        }
        self.printOutput(systemPrivateMessage)

    # Handle player hand output.
    # player is the player object.
    def playerHandOutput(self, player):
        playerObject = {
            "messageFlag": "PLAYER-HAND",
            "socketID": player.getSocketId(),
            "hand": player.getHand().getCardNamesAsJson(),
        }
        self.printOutput(playerObject)

    # Handle the Player Board output section. NOTE: need to update itemsJsonObject
    # player is the player object.
    def playerBoardOutput(self, player):
        playerObject = {
            "messageFlag": "PLAYER-BOARD",
            "playerNumber": player.getNumber(),
            "character": player.getCharacter().getJsonObject(),
            "cardCount": player.getHand().getDeckLength(),
            "coins": player.getCoins(),
            "souls": player.getSouls(),
            "items": player.getItems().getJsonObject(),
        }
        self.printOutput(playerObject)

    # Handle the treasure section output
    # treasuresBoardObject = is the treasure object. (self.activeTreasures)
    def treasureOutput(self, treasuresBoardObject):
        activeTreasureNames = []
        for i in range(len(treasuresBoardObject)):
            activeTreasureNames.append(treasuresBoardObject[i][0].getName())
        treasureOutput = {"messageFlag": "TREASURE", "treasures": activeTreasureNames}
        self.printOutput(treasureOutput)

    # Handle the Dice output
    def diceOutput(self, result):
        diceObject = {"messageFlag": "DICE", "result": result}
        self.printOutput(diceObject)

    # Handle the monster section output
    # activeMonsters is the activeMonster object - self.activeMonsters
    def monsterOutput(self, activeMonsters):
        activeMonsterList = []
        for j in range(len(activeMonsters)):
            # If the next card in the Monster Slot is an Event, construct the JSON for it - D.D.
            # HP/Attack/DiceValue are all 0, just need to show for frontend.
            # don't need to render empty json slots.
            from Events import Event
            from Enemies import Enemy

            if len(activeMonsters[j]) > 0:
                if isinstance(activeMonsters[j][0], Event):
                    monster = {
                        "cardName": activeMonsters[j][0].getName(),
                        "hp": 0,
                        "attack": 0,
                        "diceValue": 0,
                    }
                elif isinstance(activeMonsters[j][0], Enemy):
                    monster = {
                        "cardName": activeMonsters[j][0].getName(),
                        "hp": activeMonsters[j][0].getHp(),
                        "attack": activeMonsters[j][0].getAttack(),
                        "diceValue": activeMonsters[j][0].getDiceValue(),
                    }
                activeMonsterList.append(monster)
        monsterObject = {"messageFlag": "MONSTER", "monsters": activeMonsterList}
        self.printOutput(monsterObject)

    # Handle the Discard Loot Deck output
    # discardLoot is the discardLootDeck - self.discardLootDeck
    def discardLootDeckOutput(self, discardLoot):
        discardObject = {
            "messageFlag": "DISCARD-LOOT",
            "cards": discardLoot.getCardNamesAsJson(),
        }
        self.printOutput(discardObject)

    # Handle the DIscard Treasure Deck output
    # discardTreasure is the discardTreasureDeck
    def discardTreasureDeckOutput(self, discardTreasure):
        discardObject = {
            "messageFlag": "DISCARD-TREASURE",
            "cards": discardTreasure.getCardNamesAsJson(),
        }
        self.printOutput(discardObject)

    # Handle the Discard Monster Deck output.
    # discardMonster is the discardMonsterDeck
    def discardMonsterDeckOutput(self, discardMonster):
        discardObject = {
            "messageFlag": "DISCARD-MONSTER",
            "cards": discardMonster.getCardNamesAsJson(),
        }
        self.printOutput(discardObject)

    # Handle stack output.
    # stack is the stack.
    def stackOutput(self, stack):
        stackContent = {"messageFlag": "STACK", "content": stack.getStackContentJson()}
        self.printOutput(stackContent)

    def winOutput(self, player):
        winObject = {
            "messageFlag": "WINNER",
            "winnerUsername": player.getUsername(),
            "winnerCharacter": player.getCharacter().getName(),
        }
        self.printOutput(winObject)
