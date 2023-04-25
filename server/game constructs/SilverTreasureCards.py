# Jackson:  PlainSilverTreasure, DiceEffectTreasure, DeadBird, MomsBox, MomsRazor, TheRelic, StartTurnTreasure,
#           DarkBum, MonstrosTooth, EndTurnTreasure, EdensBlessing, StarterDeck, ThePolaroid, CurseOfTheTower
#
# Ethan: Finger, Fanny Pack, The Blue Map. The Compass, The Map, Charged Baby, Cambion Conception, Goat Head, Restock

from Cards import SilverTreasure
from Decks import Deck
from Effects import *
# from PIL import Image
import random

# cards that have no triggered effects
class PlainSilverTreasure(SilverTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.tag = ['no tag']
    
    def getJsonObject(self):
        silverTreasureObject = {
            "silverTreasure": super().getJsonObject(),
            "tag": self.tag
        }
        return silverTreasureObject

# cards that have an activated ability after a dice is resolved to a specific value
class DiceEffectTreasure(SilverTreasure):
    def __init__(self, name, picture, eternal, diceCheck):
        super().__init__(name, picture, eternal)
        self.diceCheck = diceCheck
        self.tag = ['dice effect']

    def getDiceCheck(self):
        return self.diceCheck
    
    def getJsonObject(self):
        diceEffectTreasureObject = {
            "silverTreasure": super().getJsonObject(),
            "tag": self.tag,
            "diceCheck": self.diceCheck
        }
        return diceEffectTreasureObject

# each time a player rolls a 2, recharge an item
class ChargedBaby(DiceEffectTreasure):
    def __init__(self, name, picture, eternal, diceCheck):
        super().__init__(name, picture, eternal, diceCheck)
        self.eternal = eternal
        self.name = name
        self.picture = picture
        self.diceCheck = diceCheck

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
        return

# each time a player rolls a 6, reveal top card of any deck, put it back or put it in the discard
class CheeseGrater(DiceEffectTreasure):
    def __init__(self, name, picture, eternal, diceCheck):
        super().__init__(name, picture, eternal, diceCheck)
        self.eternal = eternal
        self.name = name
        self.picture = picture
        self.diceCheck = diceCheck

    def use(self, user):
        board = user.getRoom().getBoard()
        choice = int(input("Choose a deck to look at the top card\n1. Loot\n2. Monster\n3. Treasure\nChoice: "))
        if choice == 1:
            # get a card from the loot deck and display the name to the player
            card = board.getLootDeck().deal()
            print(f"The loot card is {card.getName()}")
            cardDecision = int(input("Do you want to discard this card?\n1. Yes\n2. No\nChoice: "))
            if cardDecision == 1:
                # discard the card
                board.getDiscardLootDeck().addCardTop(card)
            elif cardDecision == 2:
                # put the card back on top of the deck
                board.getLootDeck().addCardTop(card)
        if choice == 2:
            # get a card from the monster deck and display the name to the player
            card = board.getMonsterDeck().deal()
            print(f"The monster card is {card.getName()}")
            cardDecision = int(input("Do you want to discard this card?\n1. Yes\n2. No\nChoice: "))
            if cardDecision == 1:
                # discard the card
                board.getDiscardMonsterDeck().addCardTop(card)
            elif cardDecision == 2:
                # put the card back on top of the deck
                board.getMonsterDeck().addCardTop(card)
        if choice == 3:
            # get a card from the treasure deck and display the name to the player
            card = board.getTreasureDeck().deal()
            print(f"The loot card is {card.getName()}")
            cardDecision = int(input("Do you want to discard this card?\n1. Yes\n2. No\nChoice: "))
            if cardDecision == 1:
                # discard the card
                board.getDiscardTreasureDeck().addCardTop(card)
            elif cardDecision == 2:
                # put the card back on top of the deck
                board.getTreasureDeck().addCardTop(card)
        return

# each time a player rolls a 3 you may loot at their hand and steal a loot card from them
class DeadBird(DiceEffectTreasure):
    def __init__(self, name, picture, eternal, diceCheck):
        super().__init__(name, picture, eternal, diceCheck)
        self.eternal = eternal
        self.name = name
        self.picture = picture
        self.diceCheck = diceCheck

    def use(self, user):
        room = user.getRoom()
        # Shows players to select from
        print("Which player do you want to steal a card from?")
        for i in range(len(room.getPlayers())):
            if room.getPlayers()[i].getCharacter().getName() == user.getCharacter().getName():
                pass
            else:
                print(f'{i + 1} :{room.getPlayers()[i].getCharacter().getName()}')
        playerChoice = int(input("Choice: "))
        print("What card from their hand do you want")
        room.getPlayers()[playerChoice - 1].getHand().printCardListNames()
        cardChoice = int(input("Choice:"))
        playerCard = room.getPlayers()[playerChoice - 1].getHand().getCard(cardChoice - 1)
        room.getPlayers()[playerChoice - 1].getHand().removeCardIndex(cardChoice - 1)
        user.getHand().addCardTop(playerCard)
        return

# each time a player rolls a 2, you may swap a non-eternal item you control with a non-eternal item they control
class Finger(DiceEffectTreasure):
    def __init__(self, name, picture, eternal, diceCheck):
        super().__init__(name, picture, eternal, diceCheck)
        self.eternal = eternal
        self.name = name
        self.picture = picture
        self.diceCheck = diceCheck

    def use(self, user):
        room = user.getRoom()
        stack = room.getStack().getStack()
        # check to make sure user doesn't swap with themselves
        if stack[-2][1].getNumber() == user.getNumber():
            print("Can't swap with yourself so nothing happened")
            return
        # have to have more than 1 item to be able to swap, 1 because always have eternal item
        if stack[-2][1].getItems().getDeckLength() < 1 or user.getItems().getDeckLength() < 1:
            print("Not enough items to swap")
            return
        choice = int(input(f"Do you want to swap an item with Player {stack[-2][1].getNumber()}\n1. Yes\n2. No\nChoice: "))
        if choice == 1:
            valid = False
            # loop to make sure they choose valid cards
            while valid is False:
                print(f"Choose which item from Player {stack[-2][1].getNumber()} to swap")
                stack[-2][1].getItems().printCardListNames()
                cardChoice = int(input("Choice: "))
                # check to make sure selected card isn't an eternal item
                print("Choose one of your items to swap")
                user.getItems().printCardListNames()
                userChoice = int(input("Choice: "))
                # check to make sure both chosen cards a not eternal, if they are break loop and go through it again
                if  stack[-2][1].getItems().getCard(cardChoice - 1).getEternal() == True:
                    print("Can't choose an eternal items from player to swap with")
                    break
                elif user.getItems().getCard(userChoice - 1).getEternal() == True:
                    print("Can't choose an eternal item from your items to swap with")
                    break
                else:
                    # save chosen card and then remove it from the player
                    choseCard = stack[-2][1].getItems().getCard(cardChoice - 1)
                    stack[-2][1].getItems().removeCardIndex(cardChoice - 1)
                    # save user chosen item and remove it from their items
                    userCard = user.getItems().getCard(userChoice - 1)
                    user.getItems().removeCardIndex(cardChoice - 1)
                    # "swap" the cards by adding it to items
                    stack[-2][1].getItems().addCardBottom(userCard)
                    user.getItems().addCardBottom(choseCard)
                    return
        else:
            print("chose to do nothing")
        return

# each time a player rolls a 4 you may loot 1 then discard a loot
class MomsBox(DiceEffectTreasure):
    def __init__(self, name, picture, eternal, diceCheck):
        super().__init__(name, picture, eternal, diceCheck)
        self.eternal = eternal
        self.name = name
        self.picture = picture
        self.diceCheck = diceCheck

    def use(self, user):
        print(f"{user.getCharacter().getName()} just gained 1 loot from {self.name}!\n")
        user.loot(1)
        # display all loot cards
        hand = user.getHand()
        hand.printCardListNames()
        # discard a card
        index = int(input("Discard which card?: "))
        index -= 1
        user.getBoard().discardLoot(user, index)
        return

# each time a player rolls a 6 you may deal 1 damage to them
class MomsRazor(DiceEffectTreasure):
    def __init__(self, name, picture, eternal, diceCheck):
        super().__init__(name, picture, eternal, diceCheck)
        self.eternal = eternal
        self.name = name
        self.picture = picture
        self.diceCheck = diceCheck

    def use(self, user):
        room = user.getRoom()
        stack = room.getStack().getStack() # i think the dice should always be at stack index -1
        choice = input(f"Do you want to deal 1 damage to Player {stack[-1][1].getNumber()}? (Y/N): ")
        if choice == "Y":
            # deal 1 damage to them
            stack[-1][1].getCharacter().takeDamage(1, user)
            print(f"Player {stack[-1][1].getNumber()} is cut by MOM'S RAZOR!\n")
        else:
            print(f"Player {stack[-1][1].getNumber()} is unaffected.\n")
        return

# each time a player rolls a 5, gains 3 cents
class EyeOfGreed(DiceEffectTreasure):
    def __init__(self, name, picture, eternal, diceCheck):
        super().__init__(name, picture, eternal, diceCheck)
        self.eternal = eternal
        self.name = name
        self.picture = picture
        self.diceCheck = diceCheck

    def use(self, user):
        print(f"{user.getCharacter().getName()} just gained 3 cents")
        user.addCoins(3)
        return

# each time a player rolls a 1, loot 1
class TheRelic(DiceEffectTreasure):
    def __init__(self, name, picture, eternal, diceCheck):
        super().__init__(name, picture, eternal, diceCheck)
        self.eternal = eternal
        self.name = name
        self.picture = picture
        self.diceCheck = diceCheck

    def use(self, user):
        print(f"{user.getCharacter().getName()} just gained 1 loot from {self.name}!\n")
        user.loot(1)
        return

def createDiceEffectTreasures():
    diceEffectDeck = Deck([])
    charged_baby = ChargedBaby("CHARGED BABY", "test image.jpg", False, 2)
    diceEffectDeck.addCardTop(charged_baby)
    cheese_grater = CheeseGrater("CHEESE GRATER", "test image.jpg", False, 6)
    diceEffectDeck.addCardTop(cheese_grater)
    dead_bird = DeadBird("DEAD BIRD", "test image.jpg", False, 3)
    diceEffectDeck.addCardTop(dead_bird)
    eye_of_greed = EyeOfGreed("EYE OF GREED", "test image.jpg", False, 5)
    diceEffectDeck.addCardTop(eye_of_greed)
    finger = Finger("FINGER", "test image.jpg", False, 2)
    diceEffectDeck.addCardTop(finger)
    moms_box = MomsBox("MOM'S BOX", "test image.jpg", False, 4)
    diceEffectDeck.addCardTop(moms_box)
    moms_razor = MomsRazor("MOM'S RAZOR", "test image.jpg", False, 6)
    diceEffectDeck.addCardTop(moms_razor)
    the_relic = TheRelic("THE RELIC", "test image.jpg", False, 1)
    diceEffectDeck.addCardTop(the_relic)
    return diceEffectDeck


# cards that have an activated ability at the start of your turn
class StartTurnTreasure(SilverTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.tag = ['start of your turn']

# at start of your turn roll...
class DarkBum(StartTurnTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user):
        from Dice import rollDice
        count = rollDice(user)
        if count < 3:
            user.addCoins(3)
            print(f"{self.name} creates riches (3c)!\n")
        elif count < 5:
            user.loot(1)
            print(f"{self.name} conjures treasures (1 loot)!\n")
        else:
            user.takeDamage(1, user)
            print(f"{self.name} takes his payment (1 damage)!!\n")
        return

# at start of your turn choose a player at random. that player destroys and item they control
class MonstrosTooth(StartTurnTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user):
        players = user.getRoom().getPlayers()
        num = random.randint(0, len(players) - 1)
        chosenPlayer = players[num]
        # make sure they have an item that can be destroyed
        if chosenPlayer.getItems().getDeckLength() > 1: # this assumes that the player will always have exactly 1 eternal item
            items = chosenPlayer.getItems()
            items.printCardListNames()
            choice = int(input(f"Player {chosenPlayer.getNumber()}, which item will you destroy?: "))
            choice -= 1
            chosenItem = items.getCardList()[choice]
            # prevent player from choosing an eternal item
            while chosenItem.getEternal() is True:
                print("You cannot choose an Eternal item.")
                choice = int(input(f"Player {chosenPlayer.getNumber()}, which item will you destroy?: "))
                choice -= 1
                chosenItem = items.getCardList()[choice]
            user.getBoard().discardTreasure(chosenPlayer, choice)
            print(f"MONSTRO destroys Player {chosenPlayer.getNumber()}'s {chosenItem.getName()}! :((\n")
        # no items that can be destroyed
        else:
            print("Nothing for MONSTRO to destroy.\n")
        return

# at start of your turn, you may put any number of shop items into the discard
class Restock(StartTurnTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user):
        room = user.getRoom()
        # Ask how many items they want to discard
        choice = int(
            input(f"There are {len(room.getBoard().getTreasures())} items in the shop. How many do you want to"
                  f" discard?\n Choice: "))
        if choice > len(room.getBoard().getTreasures()):
            print("Not enough items in shop to discard")
            return
        else:
            # Iterate the amount of cards they want to discard and having them choose shop items to discard
            for i in range(choice):
                print("Choose a shop item to discard")
                room.getBoard().displayActiveTreasures()
                discardChoice = int(input("Choice: "))
                discardedCard = room.getBoard().getTreasure(discardChoice)
                room.getBoard().clearTreasureSlot(discardChoice)
                # add item card to discard pile
                room.getBoard().getDiscardTreasureDeck().addCardTop(discardedCard)
            # re-populate the shop
            room.getBoard().checkTreasureSlots()
        return


def createStartTurnTreasures():
    startTurnDeck = Deck([])
    dark_bum = DarkBum("DARK BUM", "test image.jpg", False)
    startTurnDeck.addCardTop(dark_bum)
    monstros_tooth = MonstrosTooth("MONSTRO'S TOOTH", "test image.jpg", False)
    startTurnDeck.addCardTop(monstros_tooth)
    restock = Restock("RESTOCK", Image.open("test image.jpg"), False)
    startTurnDeck.addCardTop(restock)
    return startTurnDeck

# cards that have an activated ability at the end of your turn
class EndTurnTreasure(SilverTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.tag = ['end of your turn']

# at the end of your turn, if you have 0c gain 6c
# activates at end of turn even if owner has cents (bug but i dont think it matters)
class EdensBlessing(EndTurnTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user):
        if user.getCoins() == 0:
            print(f"{user.getCharacter().getName()} just gained 6 cents from {self.name}!\n")
            user.addCoins(6)
        else:
            print(f"{self.name} failed to activate!\n")
        return

# at the end of your turn, you may discard any number of loot cards then loot equal to amount discarded this way
class GoatHead(EndTurnTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user):
        room = user.getRoom()
        # Ask if the user wants to discard any of their cards
        choice = int(input("Do you want to dicard cards?\n1. Yes\n2. No\nChoice: "))
        #  if user want to discard
        if choice == 1:
            # ask for amount of cards they want to discard
            discardAmount = int(input(f"How many cards do you want to discard. You have {user.getHand().getDeckLength()}"
                                      f" cards in you hand\nAmount: "))
            # if don't have that many cards in their hand, cancel using the card
            if (discardAmount > user.getHand().getDeckLength()):
                print("Don't have enough cards in your hand\nCanceling...")
                return
            else:
                # loop until they discard based on amount they wanted to
                for i in range(discardAmount):
                    print("Choose a loot card to discard")
                    user.getHand().printCardListNames()
                    cardChoice = int(input("Choice: "))
                    discardedCard = user.getHand().getCard(cardChoice - 1)
                    user.getHand().removeCardIndex(cardChoice - 1)
                    # add discarded card to discard deck
                    room.getBoard().getDiscardLootDeck().addCardTop(discardedCard)
                # loot by amount of cards they discarded
                user.loot(discardAmount)
        else:
            print("Not using card")
        return

# at the end of your turn, if you have 8 loot cards or more in your hand, loot 2
class StarterDeck(EndTurnTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user):
        if user.getHand().getDeckLength() > 7:
            print(f"{user.getCharacter().getName()} adds 2 loot cards to their collection!\n")
            user.loot(2)
        else:
            print(f"{user.getCharacter().getName()} has a small collection of loot...\n")
        return

# at end of turn look at top four cards of treasure deck and put them back in any order
class TheBlueMap(EndTurnTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user):
        # use dummy deck to store order player wants cards put back
        deck = Deck([])
        dummyDeck = Deck([])
        room = user.getRoom()
        deck = user.drawTreasure(4)
        # put card in order that player wants them to be
        while deck.getDeckLength() > 0:
            deck.printCardListNames()
            index = int(input(f'Which card do you want to return to treasure deck: '))
            dummyDeck.addCardBottom(deck.getCard(index - 1))
            deck.removeCardIndex(index - 1)
        # add the cards back to the top of loot deck
        while dummyDeck.getDeckLength() > 0:
            room.getBoard().getTreasureDeck().addCardTop(dummyDeck.getCard(0))
            dummyDeck.removeCardIndex(0)
        return

# at end of turn look at top four cards of loot deck and put them back in any order
class TheCompass(EndTurnTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user):
        # use dummy deck to store order player wants cards put back
        deck = Deck([])
        dummyDeck = Deck([])
        room = user.getRoom()
        deck = user.drawLoot(4)
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
        return

# at end of turn look at top four cards of monster deck and put them back in any order
class TheMap(EndTurnTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user):
        # use dummy deck to store order player wants cards put back
        deck = Deck([])
        dummyDeck = Deck([])
        room = user.getRoom()
        deck = user.drawMonster(4)
        # put card in order that player wants them to be
        while deck.getDeckLength() > 0:
            deck.printCardListNames()
            index = int(input(f'Which card do you want to return to monster deck: '))
            dummyDeck.addCardBottom(deck.getCard(index - 1))
            deck.removeCardIndex(index - 1)
        # add the cards back to the top of monster deck
        while dummyDeck.getDeckLength() > 0:
            room.getBoard().getMonsterDeck().addCardTop(dummyDeck.getCard(0))
            dummyDeck.removeCardIndex(0)
        return

# at the end of your turn, if you have 0 loot cards in your hand, loot 2
class ThePolaroid(EndTurnTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user):
        if user.getHand().getDeckLength() == 0:
            print(f"{user.getCharacter().getName()} feels protected despite their circumstance, and finds 2 loot cards!\n")
            user.loot(2)
        else:
            print(f"{user.getCharacter().getName()} grips their loot cards...\n")
        return

def createEndTurnTreasures():
    endTurnDeck = Deck([])
    edens_blessing = EdensBlessing("EDEN'S BLESSING", "test image.jpg", False)
    endTurnDeck.addCardTop(edens_blessing)
    goat_head = GoatHead("GOAT HEAD", "test image.jpg", False)
    endTurnDeck.addCardTop(goat_head)
    starter_deck = StarterDeck("STARTER DECK", "test image.jpg", False)
    endTurnDeck.addCardTop(starter_deck)
    the_blue_map = TheBlueMap("THE BLUE MAP", "test image.jpg", False)
    endTurnDeck.addCardTop(the_blue_map)
    the_compass = TheCompass("THE COMPASS", "test image.jpg", False)
    endTurnDeck.addCardTop(the_compass)
    the_map = TheMap("THE MAP", "test image.jpg", False)
    endTurnDeck.addCardTop(the_map)
    the_polaroid = ThePolaroid("THE POLAROID", "test image.jpg", False)
    endTurnDeck.addCardTop(the_polaroid)
    return endTurnDeck

class TakeDamageTreasure(SilverTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.tag = ['take damage']

# put a counter on this card for how much damage you take, when you have 6 counters, gain 1 treasure
class CambionConception(TakeDamageTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture
        self.counter = 0

    def use(self, user, damageNum):
        self.counter += damageNum
        if self.counter >= 6:
            self.counter -= 6
            print("You have 6 or more counters! here is a treasure card")
            user.gainTreasure(1)
            print(f"You now have {self.counter} counters left")
        else:
            print(f"CAMBION CONCEPTION has {self.counter} counters")
        return

# each time you take damage roll...
class CurseOfTheTower(TakeDamageTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user, damageNum):
        players = user.getRoom().getPlayers()
        from Dice import rollDice
        count = rollDice(user)
        # each other player takes 1 damage
        if count < 4:
            print("Filled with wrath you deal 1 damage to all other players!!")
            for i in range(len(players)):
                if (i+1) != user.getNumber():
                    print(f"Player {i+1} is hurt by {self.name}!")
                    user.dealDamage(1, players[i])
        # deal 1 damage to a monster
        else:
            user.getRoom().getBoard().displayActiveMonsters()
            choice = int(input("Choose a monster to deal 1 damage to: "))
            choice -= 1
            monsters = user.getBoard().getMonsters()
            print(f"{monsters[choice][-1].getName()} is caught in your Kamikaze blast and takes 1 damage!")
            user.dealDamage(1, monsters[choice][-1])
        print("")
        return

# each time you take damage loot 1
class FannyPack(TakeDamageTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user, damageNum):
        print("Ouch! Don't worry; loot a card")
        user.loot(1)
        return

def createTakeDamageTreasures():
    takeDamageDeck = Deck([])

    cambion_conception = CambionConception("Cambion Conception", "test image.jpg", False)
    takeDamageDeck.addCardTop(cambion_conception)
    fanny_pack = FannyPack("Fanny Pack", "test image.jpg", False)
    takeDamageDeck.addCardTop(fanny_pack)
    curse_of_the_tower = CurseOfTheTower("Curse of the Tower", "test image.jpg", False)
    takeDamageDeck.addCardTop(curse_of_the_tower)
    return takeDamageDeck

def createAllSilverTreasures():
    treasureD = createDiceEffectTreasures()
    treasureS = createStartTurnTreasures()
    treasureE = createEndTurnTreasures()
    treasureTDT = createTakeDamageTreasures()
    # add all the loot cards to the same deck
    allSilverTreasures = Deck([])
    allSilverTreasures.combineDeck(treasureD)
    allSilverTreasures.combineDeck(treasureS)
    allSilverTreasures.combineDeck(treasureE)
    allSilverTreasures.combineDeck(treasureTDT)
    # allSilverTreasures.shuffle()
    return allSilverTreasures
    # return allSilverTreasures