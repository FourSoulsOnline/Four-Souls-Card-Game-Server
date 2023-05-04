# Python File to run the game - D.D.
# First will get the number of players and create a board based on it.
import sys
import time
import json
import ast
from Stack import TheStack
from Dice import Dice
# from Decks import Deck
from LootCards import createAllLootCards
from Enemies import createAllEnemies, createAdditionalEnemeies
from Events import createEventCards
from TreasureCards import createTreasureCards
from SilverTreasureCards import createAllSilverTreasures
from Board import *
from Characters import createCharactersWithNoItems
from Player import Player
from Room import Room
from JsonOutputHelper import JsonOutputHelper

Json = JsonOutputHelper()
myStack = TheStack()
myDice = Dice()

myLootDeck = createAllLootCards()
myLootDeck.shuffle()

myMonsterDeck = createAllEnemies()
newMonsters = createAdditionalEnemeies()
eventMonsters = createEventCards()
myMonsterDeck.combineDeck(newMonsters)
myMonsterDeck.combineDeck(eventMonsters)
myMonsterDeck.shuffle()

myTreasureDeck = createTreasureCards()
silverTreasures = createAllSilverTreasures()
myTreasureDeck.combineDeck(silverTreasures)
myTreasureDeck.shuffle()

characters = createCharactersWithNoItems()
characters.shuffle()


myBoard = Board(myMonsterDeck, myTreasureDeck, myLootDeck)
myBoard.checkMonsterSlotsTurnZero()
myBoard.checkTreasureSlots()
myRoom = Room(myStack, myBoard)

inputFromServer = ast.literal_eval(sys.argv[1])
# Construct players based on number of players in socket.io room - D.D.
players = []
for i in range(len(inputFromServer['players'])):
    player = Player(characters.deal(), i+1, myRoom, inputFromServer['players'][i]['socketID'], inputFromServer['players'][i]['username'])
    for i in range(3):
        player.getHand().addCardTop(myRoom.getBoard().getLootDeck().deal())
    players.append(player)
    myRoom.addPlayer(player)

playerCharacterAndUsernames = []
for player in players:
    obj = {
        "character": player.getCharacter().getName(),
        "username": player.getUsername()
    }
    playerCharacterAndUsernames.append(obj)
playersList = {
    "messageFlag": "PLAYER-LIST",
    "playersList": playerCharacterAndUsernames
}
print(json.dumps(playersList))
time.sleep(1)
sys.stdout.flush()

# Print each player hand info, and also the board info to render on the frontend - D.D.
for player in players:
    Json.playerBoardOutput(player)
    Json.playerHandOutput(player)
time.sleep(1)

myDice = Dice()
myDice.roll()

time.sleep(3)
# Start the game...
myBoard.startTurn(myRoom.getPlayers()[0])