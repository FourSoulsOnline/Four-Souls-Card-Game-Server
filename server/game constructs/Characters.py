# Contributors:
#   Jackson Cashman:
#       createCharacterCards
#   Ethan Sandoval:
#       all files
from Cards import *
from Decks import Deck
from Effects import *

def createCharacterCards():
    # characters from the base game
    # name, image, health, attack, maxAttack, starting item
    D6 = D6()
    YumHeart = YumHeart()
    SleightOfHand = SleightOfHand()
    BookOfBelial = BookOfBelial()
    ForeverAlone = ForeverAlone()
    TheCurse = TheCurse()
    BloodLust = BloodLust()
    LazarusRags = LazarusRags()
    Incubus = Incubus()
    TheBone = TheBone()
    EdenStartingCard = EdenStartingCard()
    isaac = Character("Isaac",                  "test image.jpg", 2, 1, 1, D6)
    maggy = Character("Maggy",                  "test image.jpg", 2, 1, 1, YumHeart)
    cain = Character("Cain",                    "test image.jpg", 2, 1, 1, SleightOfHand)
    judas = Character("Judas",                  "test image.jpg", 2, 1, 1, BookOfBelial)
    blue_baby = Character("Blue Baby",          "test image.jpg", 2, 1, 1, ForeverAlone)
    eve = Character("Eve",                      "test image.jpg", 2, 1, 1, TheCurse)
    samson = Character("Samson",                "test image.jpg", 2, 1, 1, BloodLust)
    lazarus = Character("Lazarus",              "test image.jpg", 2, 1, 1, LazarusRags)
    lilith = Character("Lilith",                "test image.jpg", 2, 1, 1, Incubus)
    the_forgotten = Character("The Forgotten",  "test image.jpg", 2, 1, 1, TheBone)
    eden = Character("Eden",                    "test image.jpg", 2, 1, 1, EdenStartingCard)

def createCharactersWithNoItems():
    itemMessage = "Item To Be Implemented"
    characterDeck = Deck([])
    isaac = Character("Isaac", "test image.jpg", 2, 1,  itemMessage)
    maggy = Character("Maggy", "test image.jpg", 2, 1,  itemMessage)
    cain = Character("Cain", "test image.jpg", 2, 1,  itemMessage)
    judas = Character("Judas", "test image.jpg", 2, 1,  itemMessage)
    blue_baby = Character("Blue Baby", "test image.jpg", 2, 1,  itemMessage)
    eve = Character("Eve", "test image.jpg", 2, 1,  itemMessage)
    samson = Character("Samson", "test image.jpg", 2, 1,  itemMessage)
    lazarus = Character("Lazarus", "test image.jpg", 2, 1,  itemMessage)
    lilith = Character("Lilith", "test image.jpg", 2, 1, itemMessage)
    the_forgotten = Character("The Forgotten", "test image.jpg", 2, 1,  itemMessage)
    eden = Character("Eden", "test image.jpg", 2, 1,  itemMessage)
    characterDeck.addCardTop(isaac)
    characterDeck.addCardTop(maggy)
    characterDeck.addCardTop(cain)
    characterDeck.addCardTop(judas)
    characterDeck.addCardTop(blue_baby)
    characterDeck.addCardTop(eve)
    characterDeck.addCardTop(samson)
    characterDeck.addCardTop(lazarus)
    characterDeck.addCardTop(lilith)
    characterDeck.addCardTop(the_forgotten)
    characterDeck.addCardTop(eden)
    return characterDeck

class D6(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = True
        self.name = "D6"
        self.picture = "test image.jpg"

    def use(self, user):
        # re-roll a dice roll
        room = user.getRoom()
        stack = room.getStack()
        dice = stack.findDice()
        if isinstance(dice, Dice) == True:
            dice.roll()
            self.tapped = True
        else:
            print("No dice found")
        return

class YumHeart(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = True
        self.name = "YUM HEART"
        self.picture = "test image.jpg"

    def use(self, user):
        # choose an entity to protect from an instance of damage
        room = user.getRoom()
        room.displayEntities()
        index = int(input("Who do you want to choose for Yum Heart?"))
        reduceDamage = ReduceDamage(9999)
        if isinstance(room.getEntity(index), Enemy):
            enemy = room.getEntity(index)
            enemy.addInventory(reduceDamage)
        else:
            character = room.getEntity(index)
            character.addInventory(reduceDamage)
        self.tapped = True
        return

class SleightOfHand(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = True
        self.name = "SLEIGHT OF HAND"
        self.picture = "test image.jpg"

    def use(self, user):
        # look at top 5 cards and put them back in any order
        deck = Deck([])
        dummyDeck = Deck([])
        room = user.getRoom()
        deck = user.drawLoot(5)
        # put card in order that player wants them to be
        while deck.getDeckLength() > 0:
            deck.printCardListNames()
            index = int(input(f'Which card do you want to return to loot deck: '))
            dummyDeck.addCardBottom(deck.getCard(index - 1))
            deck.removeCardIndex(index - 1)
        # add the cards back to the top of loot deck
        while dummyDeck.getDeckLength() > 0:
            room.getBoard().getLootDeck().addCardTop(dummyDeck.getCard(0))
            dummyDeck.removeCardIndex(0)
        self.tapped = True
        return

class BookOfBelial(GoldTreasure):

    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = True
        self.name = "BOOK OF BELIAL"
        self.picture = "test image.jpg"

    def use(self, user):
        # chooses to add or subtract to a die roll
        room = user.getRoom()
        stack = room.getStack()
        dice = stack.findDice()
        if isinstance(dice, Dice) == True:
            choice = int(input("1.Add to Dice roll\n2.Subtract to Dice roll\n"))
            if choice == 1:
                dice.incrementUp()
            elif choice == 2:
                dice.incrementDown()
            self.tapped = True
        else:
            print("No dice found")
        return

class ForeverAlone(GoldTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = True
        self.name = "FOREVER ALONE"
        self.picture = "test image.jpg"

    def use(self, user):
        choice = int(input("What do you want to do\nOption 1:Steal coin for a player\nOption 2:Loot at top card "
                           "of a deck\nOption 3:Discard a loot card then loot 1\nChoice: "))
        room = user.getRoom()
        # option 1 steal a coin from a player
        if choice == 1:
            print("Which player do you want to steel a coin from")
            for i in range(len(room.getPlayers())):
                if room.getPlayers()[i].getCharacter().getName() == user.getCharacter().getName():
                    pass
                else:
                    print(f'{i + 1} :{room.getPlayers()[i].getCharacter().getName()}')
            playerChoice = int(input("Choice: "))
            # steel coin from the player they choose
            if room.getPlayers()[playerChoice - 1].getCoins() == 0:
                print("This player has no coins")
                return
            else:
                room.getPlayers()[playerChoice - 1].subtractCoins(1)
                user.addCoins(1)
        # option 2 look at top card of a deck
        elif choice == 2:
            playerChoice = int(input("Which deck do you want to look at\n1.Loot deck\n2.Monster Deck\n3.Treasure Deck"
                               "\nChoice: "))
            # look at top card from deck they choose
            if playerChoice == 1:
                card = room.getBoard().getLootDeck().getCard(0)
            if playerChoice == 2:
                card = room.getBoard().getMonsterDeck().getCard(0)
            if playerChoice == 3:
                card = room.getBoard().getTreasureDeck().getCard(0)
            print(f'This is the top card from that deck: {card.getName()}')
        # option 3 discard a loot card then loot 1
        elif choice == 3:
            # if user hand is empty, then doesn't need to discard anything
            if user.getHand().getDeckLength() == 0:
                pass
            else:
                print("Which loot card do you want to discard")
                user.getHand().printCardListNames()
                playerChoice = int(input("Choice: "))
                user.getHand().removeCardIndex(playerChoice - 1)
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
        choice = int(input("Which discard deck do you want to choose\n1.Loot deck\n2.Monster Deck\n3.Treasure Deck"
                          "\nChoice: "))
        # check to make sure discard deck isn't empty, then add top card from discard back to draw deck
        if choice == 1:
            if room.getBoard().getDiscardLootDeck().getDeckLength() == 0:
                print("The Loot discard deck is empty")
            else:
                room.getBoard().getLootDeck().addCardTop(room.getBoard().getDiscardLootDeck().deal())
        elif choice == 2:
            if room.getBoard().getDiscardMonsterDeck().getDeckLength() == 0:
                print("The Monster discard deck is empty")
            else:
                room.getBoard().getMonsterDeck().addCardTop(room.getBoard().getDiscardMonsterDeck().deal())
        elif choice == 3:
            if room.getBoard().getDiscardTreasureDeck().getDeckLength() == 0:
                print("The Treasure discard deck is empty")
            else:
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
        room = user.getRoom()
        room.displayEntities()
        index = int(input("Who do you want to choose for Blood Lust?"))
        entity = room.getEntity(index)
        entity.setAttack(entity.getAttack() + 1)
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
        choice = int(input("Choose an option\n1.Swap a card from your hand with a card from another players hand"
                           "\n2.Loot one then put card from your hand to top of loot deck\nChoice: "))
        # option 1 look at a players hand and MAY swap a card with one of yours
        if choice == 1:
            # Shows players to select from
            print("Which player do you want to swap a card with")
            for i in range(len(room.getPlayers())):
                if room.getPlayers()[i].getCharacter().getName() == user.getCharacter().getName():
                    pass
                else:
                    print(f'{i + 1} :{room.getPlayers()[i].getCharacter().getName()}')
            playerChoice = int(input("Choice: "))
            print("What card from their hand do you want")
            room.getPlayers()[playerChoice - 1].getHand().printCardListNames()
            # give choice to not swap cards, they MAY
            print(f"{room.getPlayers()[playerChoice - 1].getHand().getDeckLength() + 1}:Cancel")
            cardChoice = int(input("Choice:"))
            # If they choose to cancel do nothing
            if cardChoice == room.getPlayers()[playerChoice - 1].getHand().getDeckLength() + 1:
                print("Canceling...")
                return
            else:
                playerCard = room.getPlayers()[playerChoice - 1].getHand().getCard(cardChoice - 1)
                room.getPlayers()[playerChoice - 1].getHand().removeCardIndex(cardChoice - 1)
                print("What card from your hand do you want to give them")
                user.getHand().printCardListNames()
                userChoice = int(input("Choice: "))
                userCard = user.getHand().getCard(userChoice - 1)
                user.getHand().removeCardIndex(userChoice - 1)
                room.getPlayers()[playerChoice - 1].getHand().addCardTop(userCard)
                user.getHand().addCardTop(playerCard)
        # option 2 loot one then put one card from your hand to top of loot deck
        elif choice == 2:
            user.loot(1)
            print("Choose which card to put on top of the loot deck")
            user.getHand().printCardListNames()
            index = int(input("Choice: "))
            room.getBoard().getLootDeck().addCardTop(user.getHand().getCard(index - 1))
            user.getHand().removeCardIndex(index - 1)
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
        choice = int(input("What option do you want to do\n1:Put a counter on this card\n2.Remove 1 counter,"
                           "add 1 to a dice roll\n3.Remove 2 counters, deal 1 damage to monster or player"
                           "\n4.Remove 5 counters, this card loses all abilities but becomes a soul\nChoice: "))
        # option 1 put a counter on this
        if choice == 1:
            self.counter += 1
        # option 2 remove 1 counter, add 1 to a die roll
        elif choice == 2 and self.counter >= 1:
            self.counter -= 1
            room = user.getRoom()
            stack = room.getStack()
            dice = stack.findDice()
            # look for a die and increase the number by 1
            if isinstance(dice, Dice) == True:
                dice.incrementUp()
            else:
                print("No dice found")
            return
        # option 3 remove 2 counters, deal 1 damage to monster or player
        elif choice == 3 and self.counter >= 2:
            self.counter -= 2
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
        # option 4 remove 5 counters, this becomes a soul and loses all abilities
        elif choice == 4 and self.counter >= 5:
            user.addSouls(1)
            for i in range(user.getItems().getDeckLength()):
                if user.getItems().getCard(i - 1).getName() == "THE BONE":
                    self.eternal = False
                    user.getItems().removeCardIndex(i - 1)
                # remove this card from their hand
        else:
            print("Not enough counters")
            return
        #self.tapped = True
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
    startingDeck.addCardBottom(D6("D6", "test.jpg", True))
    startingDeck.addCardBottom(YumHeart("YUM HEART", "test.jpg", True))
    startingDeck.addCardBottom(SleightOfHand("SLEIGHT OF HAND", "test.jpg", True))
    startingDeck.addCardBottom(BookOfBelial("BOOK OF BELIAL", "test.jpg", True))
    startingDeck.addCardBottom(ForeverAlone("FOREVER ALONE", "test.jpg", True))
    startingDeck.addCardBottom(TheCurse("THE CURSE", "test.jpg", True))
    startingDeck.addCardBottom(BloodLust("BLOOD LUST", "test.jpg", True))
    startingDeck.addCardBottom(LazarusRags("LAZARUS RAGS", "test.jpg", True))
    startingDeck.addCardBottom(Incubus("INCUBUS", "test.jpg", True))
    startingDeck.addCardBottom(TheBone("THE BONE", "test.jpg", True))
    startingDeck.addCardBottom(EdenStartingCard("EDEN STARTING ITEM", "test.jpg", True))
    return startingDeck