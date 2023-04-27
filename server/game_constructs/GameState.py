# Developer: Daniel De Guzman
# GameState.py - python process to create JSON of the state of the game.
import sys
import json
import ast # abstract syntax tree
import time
from Room import Room
from Board import Board
from Dice import Dice
from Player import Player
from Cards import Character
from Stack import TheStack
from LootCards import *
from Decks import Deck
from SilverTreasureCards import createAllSilverTreasures
from TreasureCards import createTreasureCards
from Enemies import *
from Characters import createCharactersWithNoItems

data_to_pass_back = 'Send this to node process.'
# Get input object from python process.
input = ast.literal_eval(sys.argv[1])
output = input
# Edit output message.
output['data_returned'] = data_to_pass_back

lootDeck = createAllLootCards()
lootDeck.shuffle()
# Send the loot deck as JSON.
output['lootDeck'] = lootDeck.getJsonObject()

characterDeck = createCharactersWithNoItems()
characterDeck.shuffle()
# Send the character deck as JSON.
output['characterDeck'] = characterDeck.getJsonObject()

treasureDeck = createTreasureCards()
treasureDeck.shuffle()
# Send the treasure deck as JSON
output['treasureDeck'] = treasureDeck.getJsonObject()

enemyDeck = createAllEnemies()
enemyDeck.shuffle()
# Send the enemy deck as JSON
output['enemyDeck'] = enemyDeck.getJsonObject()

playerCharacter = characterDeck.deal()
playerHand = Deck([])
playerHand.addCardTop(lootDeck.deal())
playerHand.addCardTop(lootDeck.deal())
playerHand.addCardTop(lootDeck.deal())
player = Player(playerCharacter, 1, "Room Code Here")
player.setHand(playerHand)
player.addToItems(treasureDeck.deal())
player.addToItems(treasureDeck.deal())
# Send the player object as JSON
output['players'][0] = player.getJsonObject()

activeTreasures = Deck([])
activeTreasures.addCardTop(treasureDeck.deal())
activeTreasures.addCardTop(treasureDeck.deal())
# Send the active treasures as JSON
output['activeTreasures'] = activeTreasures.getJsonObject()

activeEnemies = Deck([])
activeEnemies.addCardTop(enemyDeck.deal())
activeEnemies.addCardTop(enemyDeck.deal())
# Send the active treasures as JSON
output['activeEnemies'] = activeEnemies.getJsonObject()

myDice = Dice()
myDice.roll()
# Send the dice as JSON.
output['dice'] = myDice.getJsonObject()

# Output the JSON object.
print(json.dumps(output))
sys.stdout.flush()