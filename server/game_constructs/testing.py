# file for testing aspects of the game

from Cards import *

# from PIL import Image
from Decks import Deck
from Dice import Dice
from Stack import TheStack
from LootCards import *
from DeclareAttack import DeclaredAttack
from Player import Player
from Room import Room
from Board import Board
from Enemies import *
from TreasureCards import *
from SilverTreasureCards import *
from Events import createEventCards


myStack = TheStack()
myLootDeck = createAllLootCards()
myLootDeck.shuffle()
myMonsterDeck = createAllEnemies()
newMonster = createAdditionalEnemeies()
newMonster.combineDeck(myMonsterDeck)
myMonsterDeck = newMonster
eventMonster = createEventCards()
eventMonster.combineDeck(myMonsterDeck)
myMonsterDeck = eventMonster
myMonsterDeck.shuffle()
myTreasureDeck = createTreasureCards()
SilverTreasures = createAllSilverTreasures()
SilverTreasures.combineDeck(myTreasureDeck)
myTreasureDeck = SilverTreasures
# myTreasureDeck.shuffle()
myBoard = Board(myMonsterDeck, myTreasureDeck, myLootDeck)
myRoom = Room(myStack, myBoard)

isaac = Character("Isaac", "test image.jpg", 2, 1)
samson = Character("Samson", "test image.jpg", 2, 1)
maggy = Character("Maggy", "test image.jpg", 2, 1)
cain = Character("Cain", "test image.jpg", 2, 1)

player1 = Player(isaac, 1, myRoom, "1", "username")
player2 = Player(samson, 2, myRoom, "2", "username")
player3 = Player(maggy, 3, myRoom, "3", "username")
player4 = Player(cain, 4, myRoom, "4", "username")

myRoom.addPlayer(player1)
myRoom.addPlayer(player2)
myRoom.addPlayer(player3)
myRoom.addPlayer(player4)

# this needs to happen at the start of the game
myBoard.checkMonsterSlotsTurnZero()
myBoard.checkTreasureSlots()
myBoard.startTurn(player1)
