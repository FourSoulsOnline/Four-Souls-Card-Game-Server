# Contributors:
#   Jackson Cashman:
#       createCharacterCards
#   Ethan Sandoval:
#       all files
from Cards import *
from Decks import Deck
from Effects import *
from JsonOutputHelper import JsonOutputHelper
from Dice import Dice
Json = JsonOutputHelper()

def createCharacterCards():
    # characters from the base game
    # name, image, health, attack, maxAttack
    isaac = Character("Isaac",                  "test image.jpg", 2, 1, 1)
    maggy = Character("Maggy",                  "test image.jpg", 2, 1, 1)
    cain = Character("Cain",                    "test image.jpg", 2, 1, 1)
    judas = Character("Judas",                  "test image.jpg", 2, 1, 1)
    blue_baby = Character("Blue Baby",          "test image.jpg", 2, 1, 1)
    eve = Character("Eve",                      "test image.jpg", 2, 1, 1)
    samson = Character("Samson",                "test image.jpg", 2, 1, 1)
    # lazarus = Character("Lazarus",              "test image.jpg", 2, 1, 1)
    lilith = Character("Lilith",                "test image.jpg", 2, 1, 1)
    the_forgotten = Character("The Forgotten",  "test image.jpg", 2, 1, 1)
    # eden = Character("Eden",                    "test image.jpg", 2, 1, 1)

def createCharactersWithNoItems():
    characterDeck = Deck([])
    isaac = Character("Isaac", "test image.jpg", 2, 1)
    maggy = Character("Maggy", "test image.jpg", 2, 1)
    cain = Character("Cain", "test image.jpg", 2, 1)
    judas = Character("Judas", "test image.jpg", 2, 1)
    blue_baby = Character("Blue Baby", "test image.jpg", 2, 1)
    eve = Character("Eve", "test image.jpg", 2, 1)
    samson = Character("Samson", "test image.jpg", 2, 1)
    # lazarus = Character("Lazarus", "test image.jpg", 2, 1)
    lilith = Character("Lilith", "test image.jpg", 2, 1)
    the_forgotten = Character("The Forgotten", "test image.jpg", 2, 1)
    # eden = Character("Eden", "test image.jpg", 2, 1)
    characterDeck.addCardTop(isaac)
    characterDeck.addCardTop(maggy)
    characterDeck.addCardTop(cain)
    characterDeck.addCardTop(judas)
    characterDeck.addCardTop(blue_baby)
    characterDeck.addCardTop(eve)
    characterDeck.addCardTop(samson)
    # characterDeck.addCardTop(lazarus)
    characterDeck.addCardTop(lilith)
    characterDeck.addCardTop(the_forgotten)
    # characterDeck.addCardTop(eden)
    return characterDeck

class D6(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = True
        self.name = name
        self.picture = "test image.jpg"

    def use(self, user):
        # re-roll a dice roll
        room = user.getRoom()
        stack = room.getStack()
        dice = stack.findDice()
        # was getting error when playing D6, that Dice is not imported.
        from Dice import Dice
        if isinstance(dice, Dice) == True:
            dice.roll()
            message = f"the dice has been re-rolled to {dice.getResult()}"
            Json.systemOutput(message)
            self.tapped = True
        else:
            message = "No dice found"
            Json.systemOutput(message)
        return

class YumHeart(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = True
        self.name = name
        self.picture = "test image.jpg"

    def use(self, user):
        # choose an entity to protect from an instance of damage
        message = "Choose a player to give effects of Yum Heart to"
        chosenEntity = user.chooseAnyEntity(message)
        reduceDamage = ReduceDamage(9999)
        chosenEntity.addInventory(reduceDamage)
        message = f"{self.name} is protecting {chosenEntity.getName()}"
        Json.systemOutput(message)
        self.tapped = True
        return

class SleightOfHand(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = True
        self.name = name
        self.picture = "test image.jpg"

    def use(self, user):
        # look at top 5 cards and put them back in any order
        dummyDeck = Deck([])
        room = user.getRoom()
        playerOption = []
        deck = user.drawLoot(5)
        for i in deck.getCardList():
            playerOption.append(i.getName())
        # put card in order that player wants them to be
        while deck.getDeckLength() > 0:
            message = "Choose a card to return it to loot deck"
            Json.choiceOutput(user.getSocketId(), message, playerOption)
            index = int(input()) - 1
            dummyDeck.addCardBottom(deck.getCard(index))
            deck.removeCardIndex(index)
            playerOption.pop(index)
        # add the cards back to the top of loot deck
        while dummyDeck.getDeckLength() > 0:
            room.getBoard().getLootDeck().addCardTop(dummyDeck.getCard(0))
            dummyDeck.removeCardIndex(0)
        message = f"The deck has been shifted because of {self.name()}"
        Json.systemOutput(message)
        self.tapped = True
        return

class BookOfBelial(GoldTreasure):

    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = True
        self.name = name
        self.picture = "test image.jpg"

    def use(self, user):
        # chooses to add or subtract to a die roll
        room = user.getRoom()
        stack = room.getStack()
        dice = stack.findDice()
        if isinstance(dice, Dice) == True:
            message = "Choose to add or subtract 1 to the dice roll"
            Json.choiceOutput(user.getSocketId(), message, ["Add", "Subtract"])
            choice = int(input())
            if choice == 1:
                dice.incrementUp()
                message = "The dice value increased by 1"
                Json.systemOutput(message)
            elif choice == 2:
                message = "The dice value decreased by 1"
                Json.systemOutput(message)
                dice.incrementDown()
            self.tapped = True
        else:
            message = "No dice found"
            Json.systemOutput(message)
        return

class ForeverAlone(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = True
        self.name = name
        self.picture = "test image.jpg"

    def use(self, user):
        message = "Choose to steal a coin from a player, look at the top card of a deck, discard a loot card then loot 1"
        Json.choiceOutput(user.getSocketId(), message, ["Steal a coin", "Look at a deck", "Discard and Loot"])
        choice = int(input())
        room = user.getRoom()
        # option 1 steal a coin from a player
        if choice == 1:
            message = "Choose a player to steel a coin"
            Json.systemOutput(message)
            playerChoice = user.getChosenPlayer(message, user)
            # steel coin from the player they choose
            if playerChoice.getCoins() == 0:
                message = "This player has no coins"
                Json.systemOutput(message)
                return
            else:
                message = f"Player {user.getNumber()} stole 1 coin from Player {playerChoice.getNumber()}"
                Json.systemOutput(message)
                playerChoice.subtractCoins(1)
                user.addCoins(1)
        # option 2 look at top card of a deck
        elif choice == 2:
            message = "Choose a deck to look at, Loot, Monster, or Treasure"
            Json.choiceOutput(user.getSocketId(), message, ["Loot", "Monster", "Treasure"])
            deckChoice = int(input())
            # look at top card from deck they choose
            if deckChoice == 1:
                card = room.getBoard().getLootDeck().getCard(0)
            if deckChoice == 2:
                card = room.getBoard().getMonsterDeck().getCard(0)
            if deckChoice == 3:
                card = room.getBoard().getTreasureDeck().getCard(0)
            message = f"This is the top card from that deck: {card.getName()}"
            Json.systemOutput(message)
        # option 3 discard a loot card then loot 1
        elif choice == 3:
            # if user hand is empty, then doesn't need to discard anything
            if user.getHand().getDeckLength() == 0:
                message = "Your hand is empty so you don't discard"
                Json.systemOutput(message)
                pass
            else:
                message = "Choose a loot card to discard"
                playerOption = []
                for i in user.getHand().getCardList():
                    playerOption.append(i.getName())
                Json.choiceOutput(user.getSocketId(), message, playerOption)
                cardChoice = int(input())
                user.getHand().removeCardIndex(cardChoice - 1)
            message = f"Player {user.getNumber()} gained a loot from {self.name}"
            Json.systemOutput(message)
            user.loot(1)
        self.tapped = True
        return
    # somehow how to make this item recharged each time the player takes damage

class TheCurse(GoldTreasure):
    # need to implement start of turn effect (put top card of a deck into discard)
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user):
        room = user.getRoom()
        # put top card of a discard on top of its deck
        message = "Choose a discard deck to put the top card on top of it's deck"
        Json.choiceOutput(user.getSocketId(), message, ["Loot", "Monster", "Treasure"])
        choice = int(input())
        # check to make sure discard deck isn't empty, then add top card from discard back to draw deck
        if choice == 1:
            if room.getBoard().getDiscardLootDeck().getDeckLength() == 0:
                message = "The Loot discard deck is empty"
                Json.systemOutput(message)
            else:
                message = "The top card from the discard loot deck was put on top of the loot deck"
                Json.systemOutput(message)
                room.getBoard().getLootDeck().addCardTop(room.getBoard().getDiscardLootDeck().deal())
        elif choice == 2:
            if room.getBoard().getDiscardMonsterDeck().getDeckLength() == 0:
                message = "The Monster discard deck is empty"
                Json.systemOutput(message)
            else:
                message = "The top card from the discard monster deck was put on top of the monster deck"
                Json.systemOutput(message)
                room.getBoard().getMonsterDeck().addCardTop(room.getBoard().getDiscardMonsterDeck().deal())
        elif choice == 3:
            if room.getBoard().getDiscardTreasureDeck().getDeckLength() == 0:
                message = "The Treasure discard deck is empty"
                Json.systemOutput(message)
            else:
                message = "The top card from the discard treasure deck was put on top of the treasure deck"
                Json.systemOutput(message)
                room.getBoard().getTreasureDeck().addCardTop(room.getBoard().getDiscardTreasureDeck().deal())
        self.tapped = True
        return

class BloodLust(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user):
        # choose player or monster to gain 1 attack until end of turn
        message = f"Who do you want to buff with {self.name}?"
        entity = user.chooseAnyEntity(message)
        entity.setAttack(entity.getAttack() + 1)
        message = f"Player {user.getNumber()} buffed {entity.getName()}'s attack with {self.name}."
        Json.systemOutput(message)
        self.tapped = True
        return

class LazarusRags(SilverTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user):
        # when this character dies after penalties gain 1 treasure
        return

class Incubus(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user):
        room = user.getRoom()
        message = "Choose to swap a loot card with another player or loot 1 and put a card from hand on top of loot deck"
        Json.choiceOutput(user.getSocketId(), message, ["Swap", "Loot"])
        choice = int(input())
        # option 1 look at a players hand and MAY swap a card with one of yours
        if choice == 1:
            # Shows players to select from
            message = "Choose a player to swap a card with"
            playerChoice = user.getChosenPlayer(message, user)
            message = "Choose a card from their hand to swap"
            playerOption = []
            for i in playerChoice.getHand().getCardList():
                playerOption.append(i.getName())
            playerOption.append("Cancel")
            Json.choiceOutput(user.getSocketId(), message, playerOption)
            # give choice to not swap cards, they MAY
            cardChoice = int(input())
            # If they choose to cancel do nothing
            if cardChoice == playerChoice.getHand().getDeckLength() + 1:
                print("Canceling...")
                return
            else:
                playerCard = playerChoice.getHand().getCard(cardChoice - 1)
                playerCard.getHand().removeCardIndex(cardChoice - 1)
                message = "Choose a card from your hand to swap"
                playerOption = []
                for i in user.getHand().getCardList():
                    playerOption.append(i.getName())
                Json.choiceOutput(user.getSocketId(), message, playerOption)
                userChoice = int(input())
                userCard = user.getHand().getCard(userChoice - 1)
                user.getHand().removeCardIndex(userChoice - 1)
                playerChoice.getHand().addCardTop(userCard)
                user.getHand().addCardTop(playerCard)
                message = f"Player {user.getNumber()} and Player {playerChoice.getNumber()} swapped a loot card"
                Json.systemOutput(message)
        # option 2 loot one then put one card from your hand to top of loot deck
        elif choice == 2:
            user.loot(1)
            message = "Choose which card to put on top of the loot deck"
            playerOption = []
            for i in user.getHand().getCardList():
                playerOption.append(i.getName())
            Json.choiceOutput(user.getSocketId(), message, playerOption)
            index = int(input()) - 1
            room.getBoard().getLootDeck().addCardTop(user.getHand().getCard(index))
            user.getHand().removeCardIndex(index)
        self.tapped = True
        return

class TheBone(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture
        self.counter = 0

    def use(self, user):
        message = "Choose to put a counter, to remove 1 counter and add 1 to dice roll, to remove 2 counters and deal 1 " \
                  "damage to a monster or player, remove 5 counters and this card becomes a soul but loses all abilities"
        Json.choiceOutput(user.getSocketId(), message, ["+1 Counter", "-1 Add 1 dice roll", "-2 Deal 1 damage to Entity", "-5 Gain a soul"])
        choice = int(input())
        # option 1 put a counter on this
        if choice == 1:
            self.counter += 1
            message = f"A counter has been added to {self.name}"
            Json.systemOutput(message)
        # option 2 remove 1 counter, add 1 to a die roll
        elif choice == 2 and self.counter >= 1:
            self.counter -= 1
            room = user.getRoom()
            stack = room.getStack()
            dice = stack.findDice()
            # look for a die and increase the number by 1
            if isinstance(dice, Dice) == True:
                message = "Dice value was increased by 1"
                Json.systemOutput(message)
                dice.incrementUp()
            else:
                message = "No dice found"
                Json.systemOutput(message)
            return
        # option 3 remove 2 counters, deal 1 damage to monster or player
        elif choice == 3 and self.counter >= 2:
            self.counter -= 2
            # display the characters in the room
            message = f"Target which creature with {self.name}"
            chosenEntity = user.chooseAnyEntity(message)
            # Deal 1 damage to the selected target
            message = f"{self.name} did 1 damage to {chosenEntity.getName()}"
            Json.systemOutput(message)
            chosenEntity.takeDamage(1, user)
        # option 4 remove 5 counters, this becomes a soul and loses all abilities
        elif choice == 4 and self.counter >= 5:
            user.addSouls(1)
            for i in range(user.getItems().getDeckLength()):
                if user.getItems().getCard(i - 1).getName() == self.name:
                    self.eternal = False
                    user.getItems().removeCardIndex(i - 1)
                # remove this card from their hand
                Json.playerBoardOutput(user)
        else:
            message = f"Not enough counters, currently have {self.counter} counters"
            Json.systemOutput(message)
            return
        message = f"{self.name} has {self.counter} counters"
        Json.systemOutput(message)
        return

class EdenStartingCard(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user):
        # draw three treasure cards, choose one and it gets eteranl
        self.tapped = True
        return

def createAllStartingItems():
    startingDeck = Deck([])
    startingDeck.addCardBottom(D6("The D6", "test.jpg", True))
    startingDeck.addCardBottom(YumHeart("Yum Heart", "test.jpg", True))
    startingDeck.addCardBottom(SleightOfHand("Sleight Of Hand", "test.jpg", True))
    startingDeck.addCardBottom(BookOfBelial("Book Of Belial", "test.jpg", True))
    startingDeck.addCardBottom(ForeverAlone("Forever Alone", "test.jpg", True))
    startingDeck.addCardBottom(TheCurse("The Curse", "test.jpg", True))
    startingDeck.addCardBottom(BloodLust("Blood Lust", "test.jpg", True))
    startingDeck.addCardBottom(LazarusRags("Lazarus Rags", "test.jpg", True))
    startingDeck.addCardBottom(Incubus("Incubus", "test.jpg", True))
    startingDeck.addCardBottom(TheBone("The Bone", "test.jpg", True))
    startingDeck.addCardBottom(EdenStartingCard("Eden Starting Item", "test.jpg", True))
    return startingDeck