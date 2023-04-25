# Jackson: Flush! and Chaos Card
# Ethan: Everything else

from Cards import *
from Decks import Deck
from Effects import *
from Dice import *
from DeclareAttack import DeclaredAttack
import random

# Roll then either gain 1 cent, loot 1, or gain +1 hp
class BookOfSin(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Book of Sin"
        self.picture = "test image.jpg"

    def use(self, user):
        dice = Dice()
        user.addToStack(dice.roll())
        diceResult = user.getRoom().getStack().findDice().getResult()
        # gain 1 cent
        if diceResult == 1 or diceResult == 2:
            user.addCoins(1)
        # loot 1
        elif diceResult == 3 or diceResult == 4:
            user.loot(1)
        # gain +1 hp
        elif diceResult == 5 or diceResult == 6:
            user.addHp(1)
        user.getRoom().getStack().pop() # pop off the dice after it was used
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
        # Shows players to select from
        print("Which player do you want to swap a card with")
        for i in range(len(room.getPlayers())):
            if room.getPlayers()[i].getCharacter().getName() == user.getCharacter().getName():
                pass
            else:
                print(f'{i + 1} :{room.getPlayers()[i].getCharacter().getName()}')
        playerChoice = int(input("Choice: "))
        # check to see if their hand is empty
        if room.getPlayers()[playerChoice - 1].getHand().getDeckLength() == 0:
            print(f"{room.getPlayers()[playerChoice - 1].getName()} hand is empty")
        # steal a random card from selected player's hand
        else:
            player = room.getPlayers()[playerChoice - 1]
            randInt = random.randint(0, player.getHand().getDeckLength() - 1)
            randCard = player.getHand().getCard(randInt)
            player.getHand().removeCardIndex(randInt)
            user.getHand().addCardTop(randCard)
            self.tapped = True

# destroy this, you may play any number of additional loot cards till end of turn
class Box(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Box!"
        self.picture = "test image.jpg"

    def use(self, user):
        user.getCharacter().setTapped(9999)
        # destroy this item
        for i in range(user.getItems().getDeckLength()):
            if user.getItems().getCard(i - 1).getName() == "BOX!":
                user.getItems().removeCardIndex(i - 1)
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
        user.loot(1)
        print("Choose which card to put on top of the loot deck")
        user.getHand().printCardListNames()
        index = int(input("Choice: "))
        # puts chosen card on top of loot deck then removes card from player's hand
        room.getBoard().getLootDeck().addCardTop(user.getHand().getCard(index - 1))
        user.getHand().removeCardIndex(index - 1)
        self.tapped = True
        return

# each player gives hand to player on their left
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
        # choose effect
        choice = int(input("Choose: Kill a creature (1) | Destroy an item/soul (2)"))
        if choice == 1:
            room.displayEntities()
            target = int(input("Kill who?: "))
            if int(target) <= len(playerList):  # kill player
                player = room.getPlayers()[int(target) - 1]
                player.getCharacter().die(user)
            else:  # kill monster
                monster = user.getBoard().getMonsters()[int(target) - 1 - len(playerList)][-1]
                monster.die(user)
        else:
            choice = int(input("Destroy an item (1) or a soul (2)?: "))
            if choice == 1: # destroy item
                user.getRoom().displayCharacters()
                choice2 = int(input("Destroy an item from which player?: "))
                choice2 -= 1
                if playerList[choice2].getItems().getDeckLength() > 0:  # so long as the chosen player has at least 1 item
                    playerList[choice2].getItems().printCardListNames()
                    itemChoice = int(input(f"Destroy which item from player {choice2 + 1}?: "))
                    itemChoice -= 1
                    room.getBoard().discardTreasure(playerList[choice2], itemChoice)
            else: #destroy soul
                user.getRoom().displayCharacters()
                # TODO: will need to be edited when souls are made into actual cards
                choice2 = int(input("Destroy a soul from which player?: "))
                choice2 -= 1
                playerList[choice2].subtractSouls(1)
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

        choice = int(input("FLUSH! the active monster (1) or treasure (2) cards?: "))
        if choice == 1:
            # add all monsters on the board to the bottom of the deck
            for i in range(len(board.getMonsters())):
                length = len(board.getMonsters()[i])
                for j in range(length):
                    # check that the monster is not being attacked
                    if len(user.getRoom().getStack().getStack()) > 0:
                        if isinstance(user.getRoom().getStack().getStack()[0][0], DeclaredAttack):
                            if user.getRoom().getStack().getStack()[0][0].getMonster() == board.getMonsters()[i][0]:
                                pass
                            else: # there is confirmed no attack on the monster being discarded
                                monsterDeck.addCardBottom(board.getMonsters()[i][0])
            # clear out the monster slots
            for i in range(len(board.getMonsters())):
                board.getMonsters()[i] = []
            board.checkMonsterSlots(user)
            print("New monsters fill the board!\n")

        else:
            # add all treasures to the bottom of the deck
            for i in range(len(board.getTreasures())):
                treasureDeck.addCardBottom(board.getTreasures()[i][0])
            # clear out the treasure slots
            for i in range(len(board.getTreasures())):
                board.getTreasures()[i] = []
            board.checkTreasureSlots()
            print("The shop is restocked!\n")
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
        print("Which player do you want to swap a card with")
        for i in range(len(room.getPlayers())):
            if room.getPlayers()[i].getCharacter().getName() == user.getCharacter().getName():
                pass  # Don't show user in player selection
            else:
                print(f'{i + 1} :{room.getPlayers()[i].getCharacter().getName()}')
        playerChoice = int(input("Choice: "))
        # check to make sure that player has items to swap with, check is one because they will always have eternal item
        if room.getPlayers()[playerChoice - 1].getItems().getDeckLength() == 1:
            print("Player doesn't have any swappable items")
            return
        else:
            # choose an item to swap with
            print("Choose which item to steal")
            room.getPlayers()[playerChoice - 1].getItems().printCardListNames()
            cardChoice = int(input("Choice: "))
            # check to make sure selected card isn't an eternal item
            if room.getPlayers()[playerChoice - 1].getItems().getCard(cardChoice - 1).getEternal() == True:
                print("Can't choose an eternal item to swap with")
                return
            else:
                self.tapped = True
                # swap Decoy with selected Item
                # save and remove where decoy is in user's item list
                for i in range(user.getItems().getDeckLength()):
                    if user.getItems().getCard(i - 1).getName() == "DECOY":
                        decoy = user.getItems().getCard(i - 1)
                        user.getItems().removeCardIndex(i - 1)
                # save chosen card and then remove it from chosen player item deck
                choseCard = room.getPlayers()[playerChoice - 1].getItems().getCard(cardChoice - 1)
                room.getPlayers()[playerChoice - 1].getItems().removeCardIndex(cardChoice - 1)
                # give decoy to chosen player and choseCard to user
                room.getPlayers()[playerChoice - 1].getItems().addCardBottom(decoy)
                user.getItems().addCardBottom(choseCard)
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
        print("Which player do you want to destroy one of their items")
        for i in range(len(room.getPlayers())):
            if room.getPlayers()[i].getCharacter().getName() == user.getCharacter().getName():
                print(f"{i + 1} :Yourself")
            else:
                print(f'{i + 1} :{room.getPlayers()[i].getCharacter().getName()}')
        playerChoice = int(input("Choice: "))
        # check to make sure that player has items to destroy , check is one because they will always have eternal item
        if room.getPlayers()[playerChoice - 1].getItems().getDeckLength() == 1:
            print("Player doesn't have any swappable items")
            return
        else:
            # choose an item to destroy with
            print("Choose which item to destroy")
            room.getPlayers()[playerChoice - 1].getItems().printCardListNames()
            cardChoice = int(input("Choice: "))
            # check to make sure selected card isn't an eternal item
            if room.getPlayers()[playerChoice - 1].getItems().getCard(cardChoice - 1).getEternal() == True:
                print("Can't choose an eternal item to destroy")
                return
            else:
                self.tapped = True
                # destroy selected item
                room.getPlayers()[playerChoice - 1].getItems().removeCardIndex(cardChoice - 1)
                # roll a dice
                diceResult = rollDice(user)
                # if dice is a 1 - 5 then destroy this item and loot 2
                if diceResult < 6:
                    # remove this card from their items
                    for i in range(user.getItems().getDeckLength()):
                        if user.getItems().getCard(i - 1).getName() == "GLASS CANNON":
                            self.eternal = False
                            user.getItems().removeCardIndex(i - 1)
                    # then loot 2
                    user.loot(2)
                # if dice roll is a 6, recharge this item
                elif diceResult == 6:
                    self.tapped = False
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
        # loop until given valid input
        while int(val) != 1 and int(val) != 6:
            val = int(input("Do you want to change dice roll to 1 or 6: "))
        # if there is a die, update the die value
        if isinstance(dice, Dice) == True:
            dice.setResult(val)
            self.tapped = True
        else:
            print("No dice found")
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
        print("Choose a player to give you a loot card from their hand")
        for i in range(len(room.getPlayers())):
            if room.getPlayers()[i].getCharacter().getName() == user.getCharacter().getName():
                pass # don't display player using this card
            else:
                print(f'{i + 1} :{room.getPlayers()[i].getCharacter().getName()}')
        playerChoice = int(input("Choice: "))
        print(f"Player {room.getPlayers()[playerChoice - 1].getNumber()} pick a card to give to Player {user.getNumber()}")
        room.getPlayers()[playerChoice - 1].getHand().printCardListNames()
        cardChoice = int(input("Choice: "))
        user.getHand().addCardBottom(room.getPlayers()[playerChoice - 1].getHand().getCard(cardChoice - 1))
        room.getPlayers()[playerChoice - 1].getHand().removeCardIndex(cardChoice - 1)
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
            print("Not enough hp")
            return
        # choose a player prevent up to 2 damage
        user.getCharacter().setHp(user.getCharacter().getHp() - 1)
        print("Choose a player to prevent next instance of damage up to 2")
        for i in range(len(room.getPlayers())):
            if room.getPlayers()[i].getCharacter().getName() == user.getCharacter().getName():
                print(f'{i + 1} :Yourself')
            else:
                print(f'{i + 1} :{room.getPlayers()[i].getCharacter().getName()}')
        playerChoice = int(input("Choice: "))
        reduceDamage = ReduceDamage(2)
        room.getPlayers()[playerChoice - 1].getCharacter().addInventory(reduceDamage)
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
        print("Which player do you want to steel up to 3 cents from")
        # displays players
        for i in range(len(room.getPlayers())):
            if room.getPlayers()[i].getCharacter().getName() == user.getCharacter().getName():
                pass # don't display user using this item
            else:
                print(f'{i + 1} :{room.getPlayers()[i].getCharacter().getName()}')
        playerChoice = int(input("Choice: "))
        # check to see if chosen player has coins
        if room.getPlayers()[playerChoice - 1].getCoins() == 0:
            print("This player doesn't have 3 cents")
            return
        # if player has coins but less than 3, steel all their coins
        elif room.getPlayers()[playerChoice -1].getCoins() < 3:
            user.addCoins(room.getPlayers()[playerChoice - 1].getCoins())
            room.getPlayers()[playerChoice - 1].subtractCoins(room.getPlayers()[playerChoice - 1].getCoins())
        # steel 3 coin from the player they choose
        else:
            room.getPlayers()[playerChoice - 1].subtractCoins(3)
            user.addCoins(3)
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
        # loop until given valid input
        while int(val) != 1 and int(val) != 2:
            val = int(input("How much do you want to decrease; 1 or 2: "))
        # if there is a die, update the die value
        if isinstance(dice, Dice) == True:
            if val == 1:
                dice.incrementDown()
            elif val == 2:
                dice.incrementDown()
                dice.incrementDown()
            self.tapped = True
        else:
            print("No dice found")
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
        print("Which player do you want to copy one of their items")
        for i in range(len(room.getPlayers())):
            if room.getPlayers()[i].getCharacter().getName() == user.getCharacter().getName():
                print(f"{i + 1} :Yourself")
            else:
                print(f'{i + 1} :{room.getPlayers()[i].getCharacter().getName()}')
        playerChoice = int(input("Choice: "))
        # check to make sure that player has items to copy , check is one because they will always have eternal item
        if room.getPlayers()[playerChoice - 1].getItems().getDeckLength() == 1:
            print("Player doesn't have any copyable items")
            return
        else:
            # remove this card from their items, have to remove here because error when they choose to copy one of their
            # own items
            for i in range(user.getItems().getDeckLength()):
                if user.getItems().getCard(i - 1).getName() == "MODELING CLAY":
                    self.eternal = False
                    modelingClay = user.getItems().getCard(i -1)
                    user.getItems().removeCardIndex(i - 1)
            # choose an item to copy
            print("Choose which item to copy")
            room.getPlayers()[playerChoice - 1].getItems().printCardListNames()
            cardChoice = int(input("Choice: "))
            # check to make sure selected card isn't an eternal item
            if room.getPlayers()[playerChoice - 1].getItems().getCard(cardChoice - 1).getEternal() == True:
                print("Can't choose an eternal item to copy")
                # give them modeling clay back
                user.getItems().addCardBottom(modelingClay)
                return
            else:
                self.tapped = True
                # then add chosen card to copy to their items
                user.getItems().addCardBottom(room.getPlayers()[playerChoice - 1].getItems().getCard(cardChoice - 1))
                return

# deal 1 damage to a monster
class MrBoom(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Mr. Boom"
        self.picture = "test image.jpg"

    def use(self, user):
        room = user.getRoom()
        # display the active monsters
        playerList = room.getPlayers()
        monsterList = user.getBoard().getMonsters()
        for i in range(len(monsterList)):
            print(f"{i + 1}:{monsterList[i][-1].getName()}\n  HP: {monsterList[i][-1].getHp()}")
        target = int(input("Target which monster with " + str(self.getName()) + "? :"))
        # bomb monster
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
        dice = Dice()
        user.addToStack(dice.roll())
        diceResult = user.getRoom().getStack().findDice().getResult()
        # loot 1
        if diceResult == 1 or diceResult == 2:
            user.loot(1)
        # gain 4 cents
        elif diceResult == 3 or diceResult == 4:
            user.addCoins(4)
        # rolls 5 or 6 nothing happens
        else:
            print("Nothing happened")
        user.getRoom().getStack().pop()  # pop off the dice after it was used
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
        # destroy this item
        for i in range(user.getItems().getDeckLength()):
            if user.getItems().getCard(i - 1).getName() == "PANDORA'S BOX":
                self.eternal = False
                user.getItems().removeCardIndex(i - 1)
        dice = Dice()
        user.addToStack(dice.roll())
        diceResult = user.getRoom().getStack().findDice().getResult()
        # gain 1 cent
        if diceResult == 1:
            user.addCoins(1)
        # gain 6 cents
        elif diceResult == 2:
            user.addCoins(6)
        # kill a monster
        elif diceResult == 3:
            room = user.getRoom()
            room.displayEntities()
            index = int(input("Choose an character or monster to kill?"))
            room.getEntity(index).die(user)
        # gain 3 loot
        elif diceResult == 4:
            user.loot(3)
        # gain 9 cents
        elif diceResult == 5:
            user.addCoins(9)
        # this becomes a soul
        elif diceResult == 6:
            user.addSouls(1)
        user.getRoom().getStack().pop()  # pop off the dice after it was used

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
        lootCard = board.getLootDeck().deal()
        treasureCard = board.getTreasureDeck().deal()
        monsterCard = board.getMonsterDeck().deal()
        board.getDiscardLootDeck().addCardTop(lootCard)
        board.getDiscardTreasureDeck().addCardTop(treasureCard)
        board.getDiscardMonsterDeck().addCardTop(monsterCard)
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
        room = user.getRoom()
        # display the characters in the room
        playerList = room.getPlayers()
        for i in range(len(playerList)):
            print(
                f"{1 + i}: {playerList[i].getCharacter().getName()}\n  HP: {playerList[i].getCharacter().getHp()}")
        target = input("Target which player with " + str(self.getName()) + "? :")
        # deal 1 damage to selected player
        room.getPlayers()[int(target) - 1].takeDamage(1, user)
        self.tapped = True
        return

# look at the top card of a deck, you may put that card on the bottom of that deck
class SackHead(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Sack Head"
        self.picture = "test image.jpg"

    def use(self, user):
        board = user.getRoom().getBoard()
        choice = int(input("Choose a deck to look at the top card\n1. Loot\n2. Monster\n3. Treasure\nChoice: "))
        if choice == 1:
            card = board.getLootDeck().deal()
            print(f"The loot card is {card.getName()}")
            cardDecision = int(input("Do you want to put this card on the bottom of the deck?\n1. Yes\n2. No\nChoice: "))
            if cardDecision == 1:
                board.getLootDeck().addCardBottom(card)
            elif cardDecision == 2:
                board.getLootDeck().addCardTop(card)
        if choice == 2:
            card = board.getMonsterDeck().deal()
            print(f"The monster card is {card.getName()}")
            cardDecision = int(input("Do you want to put this card on the bottom of the deck?\n1. Yes\n2. No\nChoice: "))
            if cardDecision == 1:
                board.getMonsterDeck().addCardBottom(card)
            elif cardDecision == 2:
                board.getMonsterDeck().addCardTop(card)
        if choice == 3:
            card = board.getTreasureDeck().deal()
            print(f"The loot card is {card.getName()}")
            cardDecision = int(input("Do you want to put this card on the bottom of the deck?\n1. Yes\n2. No\nChoice: "))
            if cardDecision == 1:
                board.getTreasureDeck().addCardBottom(card)
            elif cardDecision == 2:
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
            print("No dice found")
        return

# Put a counter, use 3 counter and kill a player or monster
class TechX(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "Tech X"
        self.picture = "test image.jpg"
        self.counter = 0

    def use(self, user):
        choice = int(input("What do you want to do\n1.Add a counter\n2.Spend three counters "
                           "kill a monster or player"))
        # check to see if card is tapped when chosen to add a counter
        if choice == 1:
            if self.tapped == True:
                print("This card is tapped")
            else:
                self.counter += 1
                self.tapped == True
        # make sure they have enough counters to use second option
        elif choice == 2:
            if self.counter < 3:
                print("Not enough counters")
            else:
                # choose an entity and kills it
                room = user.getRoom()
                room.displayEntities()
                index = int(input("Choose an character or monster to kill?"))
                room.getEntity(index).die(user)
        return

# recharge an item
class TheBattery(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = False
        self.name = "The Battery"
        self.picture = "test image.jpg"

    def use(self, user):
        # choose an itme from all the items on the board and recharge it by setting tapped to false
        room = user.getRoom()
        allItems = Deck([])
        for i in range(len(room.getPlayers())):
            allItems.combineDeck(room.getPlayers()[i].getItems())
        print("Choose an item to recharge")
        allItems.printCardListNames()
        choice = int(input("Choice: "))
        allItems.getCard(choice - 1).setTapped(False)
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
        dice = Dice()
        user.addToStack(dice.roll())
        diceResult = user.getRoom().getStack().findDice().getResult()
        # loot 1
        if diceResult == 1:
            user.loot(1)
        # loot 2
        elif diceResult == 2:
            user.loot(2)
        # gain 3 cents
        elif diceResult == 3:
            user.addCoins(3)
        # gain 4 cents
        elif diceResult == 4:
            user.addCoins(4)
        # gain +1 hp
        elif diceResult == 5:
            user.addHp(1)
        # gain +1 attack
        elif diceResult == 6:
            user.addAttack(1)
        user.getRoom().getStack().pop()  # pop off the dice after it was used
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
        print("Choose a player re-roll an item")
        for i in range(len(room.getPlayers())):
            if room.getPlayers()[i].getCharacter().getName() == user.getCharacter().getName():
                print(f'{i + 1} :Yourself')
            else:
                print(f'{i + 1} :{room.getPlayers()[i].getCharacter().getName()}')
        playerChoice = int(input("Choice: "))
        if room.getPlayers()[playerChoice - 1].getItems().getDeckLength() < 2:
            print("Player doesn't have an item to re-roll")
            return
        print("Choose an item to re-roll")
        room.getPlayers()[playerChoice - 1].getItems().printCardListNames()
        cardChoice = int(input("Choice: "))
        room.getPlayers()[playerChoice - 1].getItems().removeCardIndex(cardChoice - 1)
        room.getPlayers()[playerChoice - 1].getItems().addCardBottom(room.getPlayers()[playerChoice - 1].drawTreasure(1))
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
        print("Choose a player to re-roll all their items")
        for i in range(len(room.getPlayers())):
            if room.getPlayers()[i].getCharacter().getName() == user.getCharacter().getName():
                print(f'{i + 1} :Yourself')
            else:
                print(f'{i + 1} :{room.getPlayers()[i].getCharacter().getName()}')
        playerChoice = int(input("Choice: "))
        if room.getPlayers()[playerChoice - 1].getItems().getDeckLength() < 2:
            print("Player doesn't have an item to re-roll")
            return
        # destroy this item
        for i in range(user.getItems().getDeckLength()):
            if user.getItems().getCard(i - 1).getName() == "THE D4":
                self.eternal = False
                user.getItems().removeCardIndex(i - 1)
        itemAmount = room.getPlayers()[playerChoice - 1].getItems().getDeckLength() - 1  # subtract because of 1 eternal
        cardsDeleted = 0
        for i in range(room.getPlayers()[playerChoice - 1].getItems().getDeckLength()):
            i -= cardsDeleted  # prevent index error as we delete items in the list
            if (room.getPlayers()[playerChoice - 1].getItems().getCard(i).getEternal() is True):
                pass # don't discard the item since it is eternal
            else:
                # discard item card to the discard pile
                card = room.getPlayers()[playerChoice - 1].getItems().getCard(i)
                room.getPlayers()[playerChoice - 1].getItems().removeCardIndex(i)
                room.getBoard().getDiscardTreasureDeck().addCardTop(card)
                cardsDeleted += 1
        # after discard all their item cards, draw treasure cards based on number of items destroyed
        for i in range(itemAmount):
            room.getPlayers()[playerChoice - 1].getItems().addCardBottom(room.getPlayers()[playerChoice - 1].drawTreasure(1))
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
            print("Not enough coins")
            return
        # subtract 4 coins and recharge an item they choose
        else:
            user.subtractCoins(4)
            room = user.getRoom()
            allItems = Deck([])
            for i in range(len(room.getPlayers())):
                allItems.combineDeck(room.getPlayers()[i].getItems())
            print("Choose an item to recharge")
            allItems.printCardListNames()
            choice = int(input("Choice: "))
            allItems.getCard(choice - 1).setTapped(False)
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
            print("Not enough items to destroy")
        else:
            # choose a player to steal one of their items
            print("Choose a player to steal one of their items")
            for i in range(len(room.getPlayers())):
                if room.getPlayers()[i].getCharacter().getName() == user.getCharacter().getName():
                    pass  # skip listing current user
                else:
                    print(f'{i + 1} :{room.getPlayers()[i].getCharacter().getName()}')
            playerChoice = int(input("Choice: "))
            if room.getPlayers()[playerChoice - 1].getItems().getDeckLength() < 2:
                print("Player doesn't have an item to re-roll")
                return
            loop = 0
            # loop until two items are destroyed
            while loop != 2:
                print("Which item do you want to destroy")
                user.getItems().printCardListNames()
                choice = int(input("Choice: "))
                if user.getItems().getCard(choice - 1).getEternal() is True:
                    print("Can't destroy an eteranl item")
                else:
                    user.getItems().removeCardIndex(choice - 1)
                    loop += 1
            # after two items are deleted, take a card from selected player
            print("Choose which item to steal")
            room.getPlayers()[playerChoice - 1].getItems().printCardListNames()
            cardChoice = int(input("Choice: "))
            user.getItems().addCardBottom(room.getPlayers()[playerChoice - 1].getItems().getCard(cardChoice - 1))
            room.getPlayers()[playerChoice - 1].getItems().removeCardIndex(cardChoice - 1)
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
            print("don't have an non-eternal item")
            return
        print("Who do you want to give an item")
        # list players for them to choose
        for i in range(len(room.getPlayers())):
            if room.getPlayers()[i].getCharacter().getName() == user.getCharacter().getName():
                pass
            else:
                print(f'{i + 1} :{room.getPlayers()[i].getCharacter().getName()}')
        playerChoice = int(input("Choice: "))
        print("which item do you want to give")
        valid = False
        # loop until they choose a non-eternal item
        while valid is False:
            user.getItems().printCardListNames()
            cardChoice = int(input("Choice: "))
            if user.getItems().getCard(cardChoice - 1).getEternal() is True:
                print("Can't choose an eternal item")
            else:
                valid = True
        # give chosen item to chosen player and remove chosen card from user who used this card
        card = user.getItems().getCard(cardChoice - 1)
        user.getItems().removeCardIndex(cardChoice - 1)
        room.getPlayers()[playerChoice - 1].getItems().addCardBottom(card)
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
            print("Don't have enough coins")
        else:
            user.subtractCoins(5)
            room = user.getRoom()
            # display the characters in the room
            playerList = room.getPlayers()
            for i in range(len(playerList)):
                print(
                    f"{1 + i}: {playerList[i].getCharacter().getName()}\n  HP: {playerList[i].getCharacter().getHp()}")
            # display the active monsters
            monsterList = user.getBoard().getMonsters()
            for i in range(len(monsterList)):
                print(f"{len(playerList) + i + 1}: {monsterList[i][-1].getName()}\n  HP: {monsterList[i][-1].getHp()}")
            target = input("Target which creature with " + str(self.getName()) + "? :")
            # bomb the selected target
            if int(target) <= len(playerList):  # deal 1 damage to player
                room.getPlayers()[int(target) - 1].takeDamage(1, user)
            else:  # deal 1 damage to monster
                user.getBoard().getMonsters()[int(target) - 1 - len(playerList)][-1].takeDamage(1, user)
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
            print("Don't have enough coins")
        else:
            # choose a player to steal one of their items
            print("Choose a player to steal one of their items")
            for i in range(len(room.getPlayers())):
                if room.getPlayers()[i].getCharacter().getName() == user.getCharacter().getName():
                    pass  # skip listing current user
                else:
                    print(f'{i + 1} :{room.getPlayers()[i].getCharacter().getName()}')
            playerChoice = int(input("Choice: "))
            if room.getPlayers()[playerChoice - 1].getItems().getDeckLength() < 2:
                print("Player doesn't have an item to re-roll")
                return
            # choose a card to steal
            print("Choose which item to steal")
            room.getPlayers()[playerChoice - 1].getItems().printCardListNames()
            cardChoice = int(input("Choice: "))
            # add chosen card to users items
            user.getItems().addCardBottom(room.getPlayers()[playerChoice - 1].getItems().getCard(cardChoice - 1))
            # remove card from chosen player items
            room.getPlayers()[playerChoice - 1].getItems().removeCardIndex(cardChoice - 1)
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
            print("Don't have enough coins")
        else:
            # subtract 3 coins then roll the dice
            user.subtractCoins(3)
            dice = Dice()
            user.addToStack(dice.roll())
            diceResult = user.getRoom().getStack().findDice().getResult()
            # loot 1
            if diceResult == 1 or diceResult == 2:
                user.loot(1)
            # gain 4 cents
            elif diceResult == 3 or diceResult == 4:
                user.addCoins(4)
            # rolls 5 or 6 nothing happens
            else:
                print("Nothing happened")
            user.getRoom().getStack().pop()  # pop off the dice after it was used
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
        print("Which loot card do you want to discard")
        user.getHand().printCardListNames()
        choice = int(input("Choice: "))
        user.getHand().removeCardIndex(choice - 1)
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

