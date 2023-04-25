# File for testing the Game

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

#bomb = Bomb("BOMB!", Image.open("test image.jpg"), 1)
#a_penny = Money("A PENNY!", Image.open("penny picture.png"), 1)
#dice_shard = DiceShard("DICE SHARD", Image.open("test image.jpg"))
#clotty1 = Enemy("CLOTTY1", Image.open("test image.jpg"), 2, 1, 1, 0, [CoinStack(4)])
#clotty6 = Enemy("CLOTTY6", Image.open("test image.jpg"), 2, 1, 6, 0, [CoinStack(4)])
#treasure1 = SilverTreasure("Silver Treasure", Image.open("test image.jpg"), False)
#treasure2 = SilverTreasure("Gold Treasure", Image.open("test image.jpg"), False)
#treasure3 = SilverTreasure("Silver Treasure", Image.open("test image.jpg"), False)
#treasure4 = SilverTreasure("Silver Treasure", Image.open("test image.jpg"), False)

myStack = TheStack()
myDice = Dice()
#myMonsterDeck = Deck([clotty1, clotty6, clotty3, clotty2])
myLootDeck = createAllLootCards()
myMonsterDeck = createAllEnemies()
myMonsterDeck.shuffle()
newMonster = createAdditionalEnemeies()
newMonster.combineDeck(myMonsterDeck)
myMonsterDeck = newMonster
#myMonsterDeck.shuffle()
myTreasureDeck = createTreasureCards()
SilverTreasures = createAllSilverTreasures()
SilverTreasures.combineDeck(myTreasureDeck)
myTreasureDeck = SilverTreasures
#myTreasureDeck.shuffle()
myBoard = Board(myMonsterDeck, myTreasureDeck, myLootDeck)
myRoom = Room(myStack, myBoard)

isaac = Character("Isaac", "test image.jpg", 2, 1, "The D6")
samson = Character("Samson", "test image.jpg", 2, 1, "Bloody Lust")
maggy = Character("Maggy", "test image.jpg", 2, 1, "Yum Heart")
the_lost = Character("The Lost", "test image.jpg", 1, 1, "Holy Mantle")

player1 = Player(isaac, 1, myRoom)
player2 = Player(samson, 2, myRoom)
player3 = Player(maggy, 3, myRoom)
player4 = Player(the_lost, 4, myRoom)

myRoom.addPlayer(player1)
myRoom.addPlayer(player2)
myRoom.addPlayer(player3)
myRoom.addPlayer(player4)

# this needs to happen at the start of the game
myBoard.checkMonsterSlots()
myBoard.checkTreasureSlots()

myBoard.startTurn(player1)


