# Jackson: Flush! and Chaos Card
# Ethan: Everything else, helped Daniel with adding JSON
# Daniel: Added JSON to cards

from Cards import *
from Decks import Deck
from Effects import *
from Dice import *
from DeclareAttack import DeclaredAttack
import random
import copy
from JsonOutputHelper import JsonOutputHelper

Json = JsonOutputHelper()


# Roll then either gain 1 cent, loot 1, or gain +1 hp
class BookOfSin(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Book of Sin"
        self.picture = "test image.jpg"

    def use(self, user):
        # roll a die
        diceResult = rollDice(user)
        # gain 1 cent
        if diceResult == 1 or diceResult == 2:
            message = "You got 1 coin"
            Json.systemOutput(message)
            user.addCoins(1)
        # loot 1
        elif diceResult == 3 or diceResult == 4:
            message = "You got a loot card"
            Json.systemOutput(message)
            user.loot(1)
        # gain +1 hp
        elif diceResult == 5 or diceResult == 6:
            message = "You gained 1 Hp until end of turn"
            Json.systemOutput(message)
            user.addHp(1)
        self.tapped = True
        return


# Choose another player then steal a random loot card from them
class Boomerang(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Boomerang"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        # create a string var to pass into JSON
        message = "Which player do you want to steal a loot card from"
        chosenPlayer = user.getChosenPlayer(message, user)
        # check to see if their hand is empty
        if chosenPlayer.getHand().getDeckLength() == 0:
            message = f"{chosenPlayer.getName()}'s hand is empty"
            Json.systemOutput(message)
        # steal a random card from selected player's hand
        else:
            # get a random number based on the number of cards is chosen player's hand
            randInt = random.randint(0, chosenPlayer.getHand().getDeckLength() - 1)
            randCard = chosenPlayer.getHand().getCard(randInt)
            chosenPlayer.getHand().removeCardIndex(randInt)
            user.getHand().addCardTop(randCard)
            message = f"Player {user.getNumber()} stole a loot card at random from Player {chosenPlayer.getNumber()}"
            Json.systemOutput(message)
            self.tapped = True
        return


# destroy this, you may play any number of additional loot cards till end of turn
class Box(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Box!"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        user.getCharacter().setTapped(9999)
        # destroy this item
        for i in range(user.getItems().getDeckLength()):
            if user.getItems().getCardList()[i] == self:
                room.getBoard().discardTreasure(user, i)
                break
        message = "The Box has been used and destroyed"
        Json.systemOutput(message)
        return


# Loot 1 then put loot card from hand on top of loot deck
class BumFriend(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Bum Friend"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        # loot a card
        user.loot(1)
        playerOptions = []
        message = "Choose which card to put on top of the loot deck"
        for i in user.getHand().getCardList():
            playerOptions.append(i.getName())
        Json.choiceOutput(user.getSocketId(), message, playerOptions)
        index = int(input())
        # puts chosen card on top of loot deck then removes card from player's hand
        room.getBoard().getLootDeck().addCardTop(user.getHand().getCard(index - 1))
        user.getHand().removeCardIndex(index - 1)
        message = "Bum Friend has been used"
        Json.systemOutput(message)
        self.tapped = True
        return


# each player gives hand to player on their left  TODO: Optimize the logic
class Chaos(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Chaos"
        self.picture = "test image.jpg"

    def use(self, user):
        # can do modulo num of players to optimize this part instead of hard coding it (try implement in future)
        room = user.getRoom()
        # p1 and p2 swap hands
        if (room.getPlayerAmount()) == 2:
            p1Hand = room.getPlayers()[0].getHand()
            p2Hand = room.getPlayers()[1].getHand()
            room.getPlayers()[0].setHand(p2Hand)
            room.getPlayers()[1].setHand(p1Hand)
        # swap p1 -> p2 -> p3 -> p1
        elif (room.getPlayerAmount()) == 3:
            p1Hand = room.getPlayers()[0].getHand()
            p2Hand = room.getPlayers()[1].getHand()
            p3Hand = room.getPlayers()[2].getHand()
            room.getPlayers()[0].setHand(p3Hand)
            room.getPlayers()[1].setHand(p1Hand)
            room.getPlayers()[2].setHand(p2Hand)
        # swap p1 -> p2 -> p3 -> p4 -> p1
        elif (room.getPlayerAmount()) == 4:
            p1Hand = room.getPlayers()[0].getHand()
            p2Hand = room.getPlayers()[1].getHand()
            p3Hand = room.getPlayers()[2].getHand()
            p4Hand = room.getPlayers()[3].getHand()
            room.getPlayers()[0].setHand(p4Hand)
            room.getPlayers()[1].setHand(p1Hand)
            room.getPlayers()[2].setHand(p2Hand)
            room.getPlayers()[3].setHand(p3Hand)
        self.tapped = True
        return


# destroy this, if you do choose one: kill a monster/play | destroy an item or soul
class ChaosCard(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Chaos Card"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        playerList = room.getPlayers()
        # destroy self
        for i in range(user.getItems().getDeckLength()):
            if user.getItems().getCardList()[i] == self:
                room.getBoard().discardTreasure(user, i)
                break
        # update player board to show card being destroyed
        Json.playerBoardOutput(user)
        # choose effect
        message = "Kill a creature or Destroy an item/soul "
        Json.choiceOutput(
            user.getSocketId(), message, ["Kill a creature", "Destroy an item/soul"]
        )
        choice = int(input())
        if choice == 1:
            playerOptions = []
            message = "Kill who?"
            # create array of strings for JSON choices entities to kill
            for i in room.getEntities():
                playerOptions.append(i.getName())
            Json.choiceOutput(user.getSocketId(), message, playerOptions)
            target = int(input())
            if int(target) <= len(playerList):  # kill player
                player = room.getPlayers()[int(target) - 1]
                player.die(user)
            else:  # kill monster
                monster = user.getBoard().getMonsters()[
                    int(target) - 1 - len(playerList)
                ][-1]
                monster.die(user)
        else:
            message = "Destroy an item or a soul?"
            Json.choiceOutput(user.getSocketId(), message, ["Item", "Soul"])
            choice = int(input())
            if choice == 1:  # destroy item
                playerOption = []
                message = "Destroy an item from which player?"
                for i in room.getPlayers():
                    playerOption.append(i.getName())
                Json.choiceOutput(user.getSocketId(), message, playerOption)
                choice2 = int(input())
                choice2 -= 1
                if (
                    playerList[choice2].getItems().getDeckLength() > 0
                ):  # so long as the chosen player has at least 1 item
                    playerOption = []
                    message = f"Destroy which item from player {choice2 + 1}?"
                    for i in playerList[choice2].getItems().getCardList():
                        playerOption.append(i.getName())
                    Json.choiceOutput(user.getSocketId(), message, playerOption)
                    itemChoice = int(input())
                    itemChoice -= 1
                    room.getBoard().discardTreasure(playerList[choice2], itemChoice)
                    message = "Chao Card has destroyed an item"
                    Json.systemOutput(message)
                else:
                    message = "chosen player doesn't have any destroyable items"
                    Json.systemOutput(message)
            else:  # destroy soul
                playerOption = []
                message = "Destroy a soul from which player?"
                for i in room.getPlayers():
                    playerOption.append(i.getName())
                Json.choiceOutput(user.getSocketId(), message, playerOption)
                choice2 = int(input())
                choice2 -= 1
                playerList[choice2].subtractSouls(1)
                message = f"Player {playerList[choice2].getNumber()} lost a soul"
                Json.systemOutput(message)
        return


# choose one: put each monster not being attacked on the bottom of the monster deck | put each shop item on the bottom of the treasure deck
class Flush(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.name = "Flush!"

    def use(self, user):
        board = user.getRoom().getBoard()
        monsterDeck = board.getMonsterDeck()
        treasureDeck = board.getTreasureDeck()
        self.tapped = True
        message = "Flush! the active monsters or treasure cards?"
        Json.choiceOutput(user.getSocketId(), message, ["Monsters", "Treasures"])
        choice = int(input())
        # CHOICE JSON
        if choice == 1:
            # add all monsters on the board to the bottom of the deck
            for i in range(len(board.getMonsters())):
                length = len(board.getMonsters()[i])
                for j in range(length):
                    # check that the monster is not being attacked
                    if len(user.getRoom().getStack().getStack()) > 0:
                        if isinstance(
                            user.getRoom().getStack().getStack()[0][0], DeclaredAttack
                        ):
                            if (
                                user.getRoom().getStack().getStack()[0][0].getMonster()
                                == board.getMonsters()[i][0]
                            ):
                                pass
                            else:  # there is confirmed no attack on the monster being discarded
                                monsterDeck.addCardBottom(board.getMonsters()[i][0])
            # clear out the monster slots
            for i in range(len(board.getMonsters())):
                board.getMonsters()[i] = []
            board.checkMonsterSlots(user)
            message = "New monsters fill the board!"
            Json.systemOutput(message)
        else:
            # add all treasures to the bottom of the deck
            for i in range(len(board.getTreasures())):
                treasureDeck.addCardBottom(board.getTreasures()[i][0])
            # clear out the treasure slots
            for i in range(len(board.getTreasures())):
                board.getTreasures()[i] = []
            board.checkTreasureSlots()
            message = "The shop is restocked!"
            Json.systemOutput(message)
        return


# Swap this card with a non-eternal item another player controls
class Decoy(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Decoy"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        # Choose a player that you want to swap an item with
        message = "Which player do you want to swap a card with"
        chosenPlayer = user.getChosenPlayer(message, user)
        # check to make sure that player has items to swap with, check is one because they will always have eternal item
        if chosenPlayer.getItems().getDeckLength() <= 1:
            message = "Player doesn't have any swappable items"
            Json.systemOutput(message)
            return
        else:
            # choose an item to swap with
            message = "Choose a card to swap with"
            playerOption = []
            for i in chosenPlayer.getItems().getCardList():
                playerOption.append(i.getName())
            Json.choiceOutput(user.getSocketId(), message, playerOption)
            cardChoice = int(input())
            # check to make sure selected card isn't an eternal item
            if chosenPlayer.getItems().getCard(cardChoice - 1).getEternal() == True:
                message = "Can't choose an eternal item to swap with"
                Json.systemOutput(message)
                return
            else:
                self.tapped = True
                # swap Decoy with selected Item
                # save and remove where decoy is in user's item list
                for i in range(user.getItems().getDeckLength()):
                    if user.getItems().getCard(i - 1).getName() == "Decoy":
                        decoy = user.getItems().getCard(i - 1)
                        user.getItems().removeCardIndex(i - 1)
                # steal the chosen card from the chosen player
                room.getBoard().stealTreasure(user, chosenPlayer, cardChoice - 1)
                # give decoy to chosen player and choseCard to user
                chosenPlayer.getItems().addCardBottom(decoy)
                message = "Decoy has been used and cards have been swapped"
                Json.systemOutput(message)
                return


# destroy another item, then roll on 1 - 5 destroy this item and loot 2 on 6 recharge this item
class GlassCannon(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Glass Cannon"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        # Choose a player that you want to destroy an item
        message = "Choose a character to destroy one of their items"
        playerOption = []
        for i in room.getPlayers():
            playerOption.append(i.getName())
        Json.choiceOutput(user.getSocketId(), message, playerOption)
        playerChoice = int(input())
        # check to make sure that player has items to destroy , check is one because they will always have eternal item
        if room.getPlayers()[playerChoice - 1].getItems().getDeckLength() <= 1:
            message = "Player doesn't have any destroyable items"
            Json.systemOutput(message)
            return
        else:
            # choose an item to destroy with
            message = "Choose an item to destroy"
            playerOption = []
            for i in room.getPlayers()[playerChoice - 1].getItems().getCardList():
                playerOption.append(i.getName())
            Json.choiceOutput(user.getSocketId(), message, playerOption)
            cardChoice = int(input())
            # check to make sure selected card isn't an eternal item
            if (
                room.getPlayers()[playerChoice - 1]
                .getItems()
                .getCard(cardChoice - 1)
                .getEternal()
                == True
            ):
                message = "Can't choose an eternal item to destroy"
                Json.systemOutput(message)
                return
            else:
                self.tapped = True
                # destroy selected item
                room.getBoard().discardTreasure(
                    room.getPlayers()[playerChoice - 1], cardChoice - 1
                )
                # roll a dice
                diceResult = rollDice(user)
                # if dice is a 1 - 5 then destroy this item and loot 2
                if diceResult < 6:
                    # remove this card from their items
                    for i in range(user.getItems().getDeckLength()):
                        if user.getItems().getCardList()[i] == self:
                            room.getBoard().discardTreasure(user, i)
                            break
                    # then loot 2
                    user.loot(2)
                    message = "Glass Cannon destroyed an item along with itself, but you looted 2"
                    Json.systemOutput(message)
                # if dice roll is a 6, recharge this item
                elif diceResult == 6:
                    self.tapped = False
                    message = "Glass Cannon destroyed an item and is ready to be used again (unless it destroyed itself)"
                    Json.systemOutput(message)
        return


# Change the result of a die to a 1 or a 6
class Godhead(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Godhead"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        stack = room.getStack()
        dice = stack.findDice()
        val = 0
        message = "Do you want to change the dice roll to a 1 or 6?"
        Json.choiceOutput(user.getSocketId(), message, ["1", "6"])
        val = int(input())
        # if there is a die, update the die value
        if isinstance(dice, Dice) == True:
            # if user chose 1, set dice value to 1
            if val == 1:
                dice.setResult(val)
            else:  # set the dice value to 6
                dice.setResult(6)
                val = 6
            self.tapped = True
            message = f"Dice result has been changed to a {val}"
            Json.systemOutput(message)
        else:
            message = "No dice found"
            Json.systemOutput(message)
        return


# choose a player, that player gives you a loot card from their hand
class GuppysHead(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Guppy's Head"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        # Choose a player to have them give the user a loot card
        message = "Choose a player to give you a loot card from their hand"
        chosenPlayer = user.getChosenPlayer(message, user)
        # have the chosen player choose a loot card to give
        message = f"Player {chosenPlayer.getNumber()} pick a card to give to Player {user.getNumber()}"
        playerOption = []
        for i in chosenPlayer.getHand().getCardList():
            playerOption.append(i.getName())
        Json.choiceOutput(chosenPlayer.getSocketId(), message, playerOption)
        cardChoice = int(input())
        # remove chosen loot card from chosen player's hand and give to the user's hand
        user.getHand().addCardBottom(chosenPlayer.getHand().getCard(cardChoice - 1))
        chosenPlayer.getHand().removeCardIndex(cardChoice - 1)
        message = f"Guppy's Head has been use and Player {user.getNumber()} was given a loot card from Player {chosenPlayer.getNumber()}"
        Json.systemOutput(message)
        self.tapped = True
        return


# pay 1 heart, choose a player, prevent next instance up to two damage they would take
class GuppysPaw(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Guppy's Paw"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        # check to see if they have hp to use the item
        if user.getCharacter().getHp() < 2:
            message = "Not enough hp"
            Json.systemOutput(message)
            return
        # choose a player prevent up to 2 damage
        user.getCharacter().setHp(user.getCharacter().getHp() - 1)
        message = "Choose a player to prevent next instance of damage up to 2"
        chosenPlayer = user.chooseAnyPlayer(message)
        # create a reduce damage object and add it to chosen player inventory
        reduceDamage = ReduceDamage(2)
        chosenPlayer.getCharacter().addInventory(reduceDamage)
        message = (
            f"{chosenPlayer.getName()} next instance of damage will be reduced by 2"
        )
        Json.systemOutput(message)
        self.tapped = True
        return


# steal 3 cents from a player
class Jawbone(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Jawbone"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        message = "Which player do you want to steel up to 3 cents from"
        chosenPlayer = user.getChosenPlayer(message, user)
        # check to see if chosen player has coins
        if chosenPlayer.getCoins() == 0:
            message = "This player doesn't have 3 cents"
            Json.systemOutput(message)
            return
        # if player has coins but less than 3, steel all their coins
        elif chosenPlayer.getCoins() < 3:
            user.addCoins(chosenPlayer.getCoins())
            chosenPlayer.subtractCoins(chosenPlayer.getCoins())
        # steel 3 coin from the player they choose
        else:
            chosenPlayer.subtractCoins(3)
            user.addCoins(3)
        message = f"Player {user.getNumber()} stole coins from Player {chosenPlayer.getNumber()}"
        Json.systemOutput(message)
        self.tapped = True
        return


# subtract up to two from a roll
class MiniMush(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Mini Mush"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        stack = room.getStack()
        dice = stack.findDice()
        val = 0
        # ask how much to decrease the dice, up to 2
        message = "How much do you want to decrease: 1 or 2?"
        Json.choiceOutput(user.getSocketId(), message, ["1", "2"])
        val = int(input())
        # if there is a die, update the die value
        if isinstance(dice, Dice) == True:
            if val == 1:
                dice.incrementDown()
                message = "Dice value has decreased by 1"
                Json.systemOutput(message)
            elif val == 2:
                dice.incrementDown()
                dice.incrementDown()
                message = "Dice value has decreased by 2"
                Json.systemOutput(message)
            self.tapped = True
        else:
            message = "No dice found"
            Json.systemOutput(message)
        return


# choose a non-eternal item, this becomes a copy of that item (permanent)
class ModelingClay(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Modeling Clay"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        # Choose a player that you want to copy an item from
        message = "Which player do you want to copy one of their items"
        chosenPlayer = user.chooseAnyPlayer(message)
        # check to make sure that player has items to copy , check is one because they will always have eternal item
        if chosenPlayer.getItems().getDeckLength() <= 1:
            message = "Player doesn't have any copyable items"
            Json.systemOutput(message)
            return
        else:
            # remove this card from their items, have to remove here because error when they choose to copy one of their
            # own items
            modelingClay = self
            for i in range(user.getItems().getDeckLength()):
                if user.getItems().getCard(i - 1).getName() == "Modeling Clay":
                    self.eternal = False
                    modelingClay = user.getItems().getCard(i - 1)
                    user.getItems().removeCardIndex(i - 1)
            Json.playerBoardOutput(user)
            # choose an item to copy
            message = "Choose which item to copy"
            playerOption = []
            for i in chosenPlayer.getItems().getCardList():
                playerOption.append(i.getName())
            Json.choiceOutput(user.getSocketId(), message, playerOption)
            cardChoice = int(input())
            # check to make sure selected card isn't an eternal item
            if chosenPlayer.getItems().getCard(cardChoice - 1).getEternal() == True:
                message = "Can't choose an eternal item to copy"
                Json.systemOutput(message)
                # give them modeling clay back
                user.getItems().addCardBottom(modelingClay)
                return
            else:
                # then add chosen card to copy to their items, use deepcopy to make sure it is a whole new card
                chosenCard = copy.deepcopy(
                    chosenPlayer.getItems().getCard(cardChoice - 1)
                )
                user.getItems().addCardBottom(chosenCard)
            return


# deal 1 damage to a monster
class MrBoom(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Mr. Boom"
        self.picture = "test image.jpg"

    def use(self, user):
        # display the active monsters
        monsterList = user.getBoard().getMonsters()
        playerOptions = []
        message = f"Target which monster with {self.getName()}?"
        for i in monsterList:
            playerOptions.append(i[-1].getName())
        Json.choiceOutput(user.getSocketId(), message, playerOptions)
        target = int(input())
        # bomb monster
        message = f"{user.getName()} did 1 damage to {user.getBoard().getMonsters()[target - 1][-1].getName()}"
        Json.systemOutput(message)
        user.getBoard().getMonsters()[target - 1][-1].takeDamage(1, user)
        self.tapped = True
        return


# roll a die, 1-2 loot 1 and 3-4 gain 4 cents
class MysterySack(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Mystery Sack"
        self.picture = "test image.jpg"

    def use(self, user):
        diceResult = rollDice(user)
        # loot 1
        if diceResult == 1 or diceResult == 2:
            message = "You got a loot card"
            Json.systemOutput(message)
            user.loot(1)
        # gain 4 cents
        elif diceResult == 3 or diceResult == 4:
            message = "added 5 coins"
            Json.systemOutput(message)
            user.addCoins(4)
        # rolls 5 or 6 nothing happens
        else:
            message = "Nothing happened"
            Json.systemOutput(message)
        self.tapped = True
        return


# destroy this then roll, 1: gain 1 cent, 2: gain 6 cents, 3: kill a monster, 4: loot 3, 5: gain 9 cents,
# 6: this becomes a soul
class PandorasBox(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Pandora's Box"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        # destroy this item
        for i in range(user.getItems().getDeckLength()):
            if user.getItems().getCardList()[i] == self:
                room.getBoard().discardTreasure(user, i)
                break
        Json.playerBoardOutput(user)
        diceResult = rollDice(user)
        # gain 1 cent
        if diceResult == 1:
            message = "You gained 1 coin"
            Json.systemOutput(message)
            user.addCoins(1)
        # gain 6 cents
        elif diceResult == 2:
            message = "You gained 6 coins"
            Json.systemOutput(message)
            user.addCoins(6)
        # kill a monster
        elif diceResult == 3:
            monsterList = user.getBoard().getMonsters()
            message = "Choose a monster to kill"
            playerOptions = []
            for i in monsterList:
                playerOptions.append(i[-1].getName())
            Json.choiceOutput(user.getSocketId(), message, playerOptions)
            target = int(input())
            user.getBoard().getMonsters()[target - 1][-1].die(user)
        # gain 3 loot
        elif diceResult == 4:
            message = "You gained 3 loot cards"
            Json.systemOutput(message)
            user.loot(3)
        # gain 9 cents
        elif diceResult == 5:
            message = "You gained 9 coins"
            Json.systemOutput(message)
            user.addCoins(9)
        # this becomes a soul
        elif diceResult == 6:
            message = "You got 1 soul!"
            Json.systemOutput(message)
            user.addSouls(1)
        return


# put the top card of each deck into discard
class PotatoPeeler(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Potato Peeler"
        self.picture = "test image.jpg"

    def use(self, user):
        # get the top card from all deck then discard them to their respectful deck
        board = user.getRoom().getBoard()
        # get top card from each deck
        lootCard = board.getLootDeck().deal()
        treasureCard = board.getTreasureDeck().deal()
        monsterCard = board.getMonsterDeck().deal()
        # add the card to the discard of each deck
        board.getDiscardLootDeck().addCardTop(lootCard)
        board.getDiscardTreasureDeck().addCardTop(treasureCard)
        board.getDiscardMonsterDeck().addCardTop(monsterCard)
        message = f"Top cards of all decks were discarded by {self.getName()}"
        Json.systemOutput(message)
        self.tapped = True
        return


# deal 1 damage to a player
class RazorBlade(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Razor Blade"
        self.picture = "test image.jpg"

    def use(self, user):
        # get a player
        message = "Choose a player to take 1 damage"
        chosenPlayer = user.chooseAnyPlayer(message)
        # deal 1 damage to selected player
        message = f"Razor Blade did 1 damage to {chosenPlayer.getName()}"
        Json.systemOutput(message)
        chosenPlayer.takeDamage(1, user)
        self.tapped = True
        return


# look at the top card of a deck, you may put that card on the bottom of that deck
# TODO: check to see if we can display the card itself instead of just saying card name in options
class SackHead(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Sack Head"
        self.picture = "test image.jpg"

    def use(self, user):
        board = user.getRoom().getBoard()
        # ask user what deck they want to look top card of
        message = "Choose a deck to look at the top card: Loot, Monster, Treasure"
        Json.choiceOutput(user.getSocketId(), message, ["Loot", "Monster", "Treasure"])
        choice = int(input())
        # CHOICE JSON
        # enter loot deck option
        if choice == 1:
            card = board.getLootDeck().deal()
            message = f"The loot card is {card.getName()}. Put it on the top or bottom of the deck?"
            Json.choiceOutput(user.getSocketId(), message, ["Bottom", "Top"])
            cardDecision = int(input())
            # add card to bottom of loot deck
            if cardDecision == 1:
                message = f"{card.getName()} was put at the bottom of the loot deck"
                Json.systemOutput(message)
                board.getLootDeck().addCardBottom(card)
            # add card back to top of loot deck
            elif cardDecision == 2:
                message = f"{card.getName()} was put at the top of the loot deck"
                Json.systemOutput(message)
                board.getLootDeck().addCardTop(card)
        # enter monster deck option
        if choice == 2:
            card = board.getMonsterDeck().deal()
            message = f"The monster card is {card.getName()}. Put it on the top or bottom of the deck?"
            Json.choiceOutput(user.getSocketId(), message, ["Bottom", "Top"])
            cardDecision = int(input())
            # add card to bottom of monster deck
            if cardDecision == 1:
                message = f"{card.getName()} was put at the bottom of the monster deck"
                Json.systemOutput(message)
                board.getMonsterDeck().addCardBottom(card)
            # add card back to top of monster deck
            elif cardDecision == 2:
                message = f"{card.getName()} was put at the top of the monster deck"
                Json.systemOutput(message)
                board.getMonsterDeck().addCardTop(card)
        # enter treasure deck option
        if choice == 3:
            card = board.getTreasureDeck().deal()
            message = f"The treasure card is {card.getName()}. Put it on the top or bottom of the deck?"
            Json.choiceOutput(user.getSocketId(), message, ["Bottom", "Top"])
            cardDecision = int(input())
            # add card to bottom of treasure deck
            if cardDecision == 1:
                message = f"{card.getName()} was put at the bottom of the treasure deck"
                Json.systemOutput(message)
                board.getTreasureDeck().addCardBottom(card)
            # add card back to top of treasure deck
            elif cardDecision == 2:
                message = f"{card.getName()} was put at the top of the treasure deck"
                Json.systemOutput(message)
                board.getTreasureDeck().addCardTop(card)
        self.tapped = True
        return


# add 1 to a roll
class SpoonBender(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Spoon Bender"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        stack = room.getStack()
        dice = stack.findDice()
        # look for a die and increase the number by 1
        if isinstance(dice, Dice) == True:
            dice.incrementUp()
            self.tapped = True
        else:
            message = "No dice found"
            Json.systemOutput(message)
        return


# Put a counter, use 3 counter and kill a player or monster
class TechX(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Tech X"
        self.picture = "test image.jpg"
        self.counter = 3

    def use(self, user):
        message = (
            "Choose to add a counter or spend 3 counters to kill a player or monster"
        )
        Json.choiceOutput(
            user.getSocketId(), message, ["Add a counter", "Kill monster or player"]
        )
        choice = int(input())
        # check to see if card is tapped when chosen to add a counter
        if choice == 1:
            if self.tapped == True:
                message = "This card is tapped"
                Json.systemOutput(message)
            else:
                self.counter += 1
                self.tapped == True
        # make sure they have enough counters to use second option
        elif choice == 2:
            if self.counter < 3:
                message = "Not enough counters"
                Json.systemOutput(message)
            else:
                # choose an entity and kills it
                self.counter -= 3
                message = "Choose an character or monster to kill?"
                chosenEntity = user.chooseAnyEntity(message)
                chosenEntity.die(user)
        return


# recharge an item, think this works because when adding all cards to a separate deck, it makes a shallow copy
class TheBattery(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "The Battery"
        self.picture = "test image.jpg"

    def use(self, user):
        # choose an item from all the items on the board and recharge it by setting tapped to false
        room = user.getRoom()
        allItems = Deck([])
        itemChoice = []
        # create a deck with all items on the board
        for i in range(len(room.getPlayers())):
            allItems.combineDeck(room.getPlayers()[i].getItems())
        # create an array of string of all items to pass into JSON
        for i in allItems.getCardList():
            itemChoice.append(i.getName())
        message = "Choose an item to recharge"
        Json.choiceOutput(user.getSocketId(), message, itemChoice)
        choice = int(input())
        # Check to see if they choose a passive item to prevent an error
        if isinstance(allItems.getCard(choice - 1), SilverTreasure):
            message = "Can't recharge a passive item"
            Json.systemOutput(message)
            return
        allItems.getCard(choice - 1).setTapped(False)
        message = f"{allItems.getCard(choice - 1).getName()} has been recharged"
        Json.systemOutput(message)
        self.tapped = True
        return


# roll a die, 1: loot 1, 2: loot 2, 3: gain 3 cents, 4: gain 4 cents, 5: gain 1 hp until end of turn,
# 6: gain 1 attack until end of turn
class TheD100(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "The D100"
        self.picture = "test image.jpg"

    def use(self, user):
        diceResult = rollDice(user)
        # loot 1
        if diceResult == 1:
            message = "You gained a loot card"
            Json.systemOutput(message)
            user.loot(1)
        # loot 2
        elif diceResult == 2:
            message = "You gained 2 loot cards"
            Json.systemOutput(message)
            user.loot(2)
        # gain 3 cents
        elif diceResult == 3:
            message = "You gained 3 coins"
            Json.systemOutput(message)
            user.addCoins(3)
        # gain 4 cents
        elif diceResult == 4:
            message = "You gained 4 coins"
            Json.systemOutput(message)
            user.addCoins(4)
        # gain +1 hp
        elif diceResult == 5:
            message = "You gained 1 hp until end of turn"
            Json.systemOutput(message)
            user.addHp(1)
        # gain +1 attack
        elif diceResult == 6:
            message = "You gained 1 attack until end of turn"
            Json.systemOutput(message)
            user.addAttack(1)
        self.tapped = True
        return


# re-roll an item (destroys an item then replaces it with top card from treasure deck)
class TheD20(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "The D20"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        # choose a player to re-roll one of their items
        message = "Choose a player re-roll an item"
        playerChoice = user.chooseAnyPlayer(message)
        if playerChoice.getItems().getDeckLength() < 2:
            message = "Player doesn't have an item to re-roll"
            Json.systemOutput(message)
            return
        # choose item from chosen player to re-roll one of their items
        message = "Choose an item to re-roll"
        playerOptions = []
        for i in playerChoice.getItems().getCardList():
            playerOptions.append(i.getName())
        Json.choiceOutput(user.getSocketId(), message, playerOptions)
        cardChoice = int(input())
        # make sure they can't destroy an eternal item
        if playerChoice.getItems().getCard(cardChoice - 1).getEternal() == True:
            message = "Can't choose an eternal item to destroy"
            Json.systemOutput(message)
            return
        # discard the chosen item and then give chosen player item from top of treasure deck
        room.getBoard().discardTreasure(playerChoice, cardChoice - 1)
        playerChoice.getItems().addCardBottom(playerChoice.drawTreasure(1))
        message = "An item got re-rolled"
        Json.systemOutput(message)
        self.tapped = True
        return


# destroy this, choose a player, re-roll each item they own (except for eternal item)
class TheD4(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "The D4"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        # choose a player to re-roll all of their items
        message = "Choose a player to re-roll all their items"
        playerChoice = user.chooseAnyPlayer(message)
        if playerChoice.getItems().getDeckLength() < 2:
            message = "Player doesn't have an item to re-roll"
            Json.systemOutput(message)
            return
        # destroy this item
        for i in range(user.getItems().getDeckLength()):
            if user.getItems().getCard(i - 1).getName() == "The D4":
                self.eternal = False
                user.getItems().removeCardIndex(i - 1)
        Json.playerBoardOutput(user)
        itemAmount = (
            playerChoice.getItems().getDeckLength() - 1
        )  # subtract because of 1 eternal
        cardsDeleted = 0
        for i in range(playerChoice.getItems().getDeckLength()):
            i -= cardsDeleted  # prevent index error as we delete items in the list
            if playerChoice.getItems().getCard(i).getEternal() is True:
                pass  # don't discard the item since it is eternal
            else:
                # discard the treasure card
                room.getBoard().discardTreasure(playerChoice, i)
                cardsDeleted += 1
        # after discard all their item cards, draw treasure cards based on number of items discarded
        for i in range(itemAmount):
            playerChoice.getItems().addCardBottom(playerChoice.drawTreasure(1))
        message = f"Player {playerChoice.getNumber()} had all their items rerolled"
        Json.systemOutput(message)
        return


# pay 4 cents, recharge an item
class BatteryBum(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Battery Bum"
        self.picture = "test image.jpg"

    def use(self, user):
        # check to make sure they have enough coins
        if user.getCoins() < 4:
            message = "Not enough coins"
            Json.systemOutput(message)
            return
        # subtract 4 coins and recharge an item they choose
        else:
            user.subtractCoins(4)
            room = user.getRoom()
            allItems = Deck([])
            itemChoice = []
            # create a deck with all items on the board
            for i in range(len(room.getPlayers())):
                allItems.combineDeck(room.getPlayers()[i].getItems())
            # create an array of string of all items to pass into JSON
            for i in allItems.getCardList():
                itemChoice.append(i.getName())
            message = "Choose an item to recharge"
            Json.choiceOutput(user.getSocketId(), message, itemChoice)
            choice = int(input())
            # Check to see if they choose a passive item to prevent an error
            if isinstance(allItems.getCard(choice - 1), SilverTreasure):
                message = "Can't recharge a passive item"
                Json.systemOutput(message)
                return
            allItems.getCard(choice - 1).setTapped(False)
            message = f"{allItems.getCard(choice - 1).getName()} has been recharged"
            Json.systemOutput(message)
        return


# Destroy two items you control, steal a non-eternal item
class ContractFromBelow(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Contract From Below"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        if user.getItems().getDeckLength() < 2:
            message = "Not enough items to destroy"
            Json.systemOutput(message)
        else:
            # choose a player to steal one of their items
            message = "Choose a player to steal one of their items"
            playerChoice = user.getChosenPlayer(message, user)
            if playerChoice.getItems().getDeckLength() < 2:
                message = "Player doesn't have an item to steal"
                Json.systemOutput(message)
                return
            loop = 0
            # loop until two items are destroyed
            while loop != 2:
                message = "Which item do you want to destroy"
                playerOption = []
                for i in user.getItems().getCardList():
                    playerOption.append(i.getName())
                Json.choiceOutput(user.getSocketId(), message, playerOption)
                choice = int(input())
                if user.getItems().getCard(choice - 1).getEternal() is True:
                    message = "Can't destroy an eteranl item"
                    Json.systemOutput(message)
                else:
                    room.getBoard().discardTreasure(user, choice - 1)
                    loop += 1
            # after two items are deleted, take a card from selected player
            valid = False
            while valid is False:
                message = "Choose which item to steal"
                playerOption = []
                for i in playerChoice.getItems().getCardList():
                    playerOption.append(i.getName())
                Json.choiceOutput(user.getSocketId(), message, playerOption)
                cardChoice = int(input())
                # check to make sure they don't steal an eternal item
                if playerChoice.getItems().getCard(cardChoice - 1).getEternal() == True:
                    message = "Can't choose an eternal item to steal"
                    Json.systemOutput(message)
                    return
                # steal the chosen card from the chosen player
                valid = True
                message = (
                    f"Player {user.getNumber()} stole "
                    f"{playerChoice.getItems().getCard(cardChoice - 1).getName()} from Player"
                    f" {playerChoice.getNumber()}"
                )
                Json.systemOutput(message)
                room.getBoard().stealTreasure(user, playerChoice, cardChoice - 1)
        return


# give another player a non-eternal item you control, gain 8 cents
class DonationMachine(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Donation Machine"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        # user will always have 1 eternal item, need at least another item
        if user.getItems().getDeckLength() < 2:
            message = "don't have an non-eternal item"
            Json.systemOutput(message)
            return
        message = "Who do you want to give an item"
        playerChoice = user.getChosenPlayer(message, user)
        message = "choose an item do you want to give"
        valid = False
        # loop until they choose a non-eternal item
        while valid is False:
            playerOption = []
            for i in user.getItems().getCardList():
                playerOption.append(i.getName())
            Json.choiceOutput(user.getSocketId(), message, playerOption)
            cardChoice = int(input())
            if user.getItems().getCard(cardChoice - 1).getEternal() is True:
                message = "Can't choose an eternal item"
                Json.systemOutput(message)
            else:
                valid = True
        # have chosen player steal card from the use
        message = (
            f"Player {user.getNumber()} gained 8 coins but has given "
            f"{user.getItems().getCard(cardChoice - 1).getName()} to Player {playerChoice.getNumber()}"
        )
        Json.systemOutput(message)
        room.getBoard().stealTreasure(playerChoice, user, cardChoice - 1)
        user.addCoins(8)
        return


# Pay 5 cents, deal 1 damage to monster or player
class GoldenRazorBlade(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Golden Razor Blade"
        self.picture = "test image.jpg"

    def use(self, user):
        if user.getCoins() < 5:
            message = "Don't have enough coins"
            Json.systemOutput(message)
        else:
            user.subtractCoins(5)
            # display the characters in the room
            message = f"Target which creature with {self.name}"
            chosenEntity = user.chooseAnyEntity(message)
            # Golden Razor the selected target
            message = f"{self.name} did 1 damage to {chosenEntity.getName()}"
            Json.systemOutput(message)
            chosenEntity.takeDamage(1, user)
        return


# pay 10 cents, steal a non-eternal item a player controls
class PayToPlay(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Pay to Play"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        if user.getCoins() < 10:
            message = "Don't have enough coins"
            Json.systemOutput(message)
        else:
            # choose a player to steal one of their items
            message = "Choose a player to steal one of their items"
            playerChoice = user.getChosenPlayer(message, user)
            if playerChoice.getItems().getDeckLength() < 2:
                message = "Player doesn't have an item to re-roll"
                Json.systemOutput(message)
                return
            # choose a card to steal
            message = "Choose which item to steal"
            playerOption = []
            for i in playerChoice.getItems().getCardList():
                playerOption.append(i.getName())
            Json.choiceOutput(user.getSocketId(), message, playerOption)
            cardChoice = int(input())
            # check to make sure they don't steal an eternal item
            if playerChoice.getItems().getCard(cardChoice - 1).getEternal() == True:
                message = "Can't choose an eternal item to steal"
                Json.systemOutput(message)
                return
            # steal stolen treasure from chosen player
            message = (
                f"Player {user.getNumber()} spent 10 coins to steal "
                f"{playerChoice.getItems().getCard(cardChoice - 1).getName()} "
                f"from Player {playerChoice.getNumber()}"
            )
            Json.systemOutput(message)
            room.getBoard().stealTreasure(user, playerChoice, cardChoice - 1)
            user.subtractCoins(10)
        return


# pay 3 cents roll, 1-2 loot 1, 3-4 gain 4 cents
class PortableSlotMachine(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Portable Slot Machine"
        self.picture = "test image.jpg"

    def use(self, user):
        if user.getCoins() < 3:
            message = "Don't have enough coins"
            Json.systemOutput(message)
        else:
            # subtract 3 coins then roll the dice
            user.subtractCoins(3)
            diceResult = rollDice(user)
            # loot 1
            if diceResult == 1 or diceResult == 2:
                message = "You gained a loot card"
                Json.systemOutput(message)
                user.loot(1)
            # gain 4 cents
            elif diceResult == 3 or diceResult == 4:
                message = "You gained 4 coins"
                Json.systemOutput(message)
                user.addCoins(4)
            # rolls 5 or 6 nothing happens
            else:
                message = "Nothing happened"
                Json.systemOutput(message)
        return


# discard a loot card, gain three cents
class Smelter(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Smelter"
        self.picture = "test image.jpg"

    def use(self, user):
        # ask for a loot card from their hand to discard, then gain 3 cents
        message = "Choose a loot card do you want to discard"
        playerOption = []
        for i in user.getHand().getCardList():
            playerOption.append(i.getName())
        Json.choiceOutput(user.getSocketId(), message, playerOption)
        choice = int(input())
        message = f"Player {user.getNumber()} discarded {user.getHand().getCard(choice - 1).getName()} for 3 cents"
        Json.systemOutput(message)
        # save card to put in discard deck
        card = user.getHand().getCard(choice - 1)
        # remove card from user's hand
        user.getHand().removeCardIndex(choice - 1)
        # add card to loot discard deck and then have user gain 3 coins
        user.getRoom().getBoard().getDiscardLootDeck().addCardTop(card)
        user.addCoins(3)
        return


def createTreasureCards():
    treasureDeck = Deck([])
    treasureDeck.addCardBottom(BookOfSin(" ", " ", False))
    treasureDeck.addCardBottom(Boomerang(" ", " ", False))
    treasureDeck.addCardBottom(Box(" ", " ", False))
    treasureDeck.addCardBottom(BumFriend(" ", " ", False))
    treasureDeck.addCardBottom(Chaos(" ", " ", False))
    treasureDeck.addCardBottom(ChaosCard("Chaos Card", "test image.jpg", False))
    treasureDeck.addCardBottom(Decoy(" ", " ", False))
    treasureDeck.addCardBottom(Flush("Flush!", "test image.jpg", False))
    treasureDeck.addCardBottom(GlassCannon(" ", " ", False))
    treasureDeck.addCardBottom(Godhead(" ", " ", False))
    treasureDeck.addCardBottom(GuppysHead(" ", " ", False))
    treasureDeck.addCardBottom(GuppysPaw(" ", " ", False))
    treasureDeck.addCardBottom(Jawbone(" ", " ", False))
    treasureDeck.addCardBottom(MiniMush(" ", " ", False))
    treasureDeck.addCardBottom(ModelingClay(" ", " ", False))
    treasureDeck.addCardBottom(MrBoom(" ", " ", False))
    treasureDeck.addCardBottom(MysterySack(" ", " ", False))
    treasureDeck.addCardBottom(PandorasBox(" ", " ", False))
    treasureDeck.addCardBottom(PotatoPeeler(" ", " ", False))
    treasureDeck.addCardBottom(RazorBlade(" ", " ", False))
    treasureDeck.addCardBottom(SackHead(" ", " ", False))
    treasureDeck.addCardBottom(SpoonBender(" ", " ", False))
    treasureDeck.addCardBottom(TechX(" ", " ", False))
    treasureDeck.addCardBottom(TheBattery(" ", " ", False))
    treasureDeck.addCardBottom(TheD100(" ", " ", False))
    treasureDeck.addCardBottom(TheD20(" ", " ", False))
    treasureDeck.addCardBottom(TheD4(" ", " ", False))
    treasureDeck.addCardBottom(BatteryBum(" ", " ", False))
    treasureDeck.addCardBottom(ContractFromBelow(" ", " ", False))
    treasureDeck.addCardBottom(DonationMachine(" ", " ", False))
    treasureDeck.addCardBottom(GoldenRazorBlade(" ", " ", False))
    treasureDeck.addCardBottom(PayToPlay(" ", " ", False))
    treasureDeck.addCardBottom(PortableSlotMachine(" ", " ", False))
    treasureDeck.addCardBottom(Smelter(" ", " ", False))
    return treasureDeck
