# Jackson:  PlainSilverTreasure, DiceEffectTreasure, DeadBird, MomsBox, MomsRazor, TheRelic, StartTurnTreasure,
#           DarkBum, MonstrosTooth, EndTurnTreasure, EdensBlessing, StarterDeck, ThePolaroid, CurseOfTheTower
#
# Ethan: Finger, Fanny Pack, The Blue Map. The Compass, The Map, Charged Baby, Cambion Conception, Goat Head, Restock

from Cards import SilverTreasure
from Decks import Deck
from Effects import *
from JsonOutputHelper import JsonOutputHelper
# from PIL import Image
import random

Json = JsonOutputHelper()

# cards that have no triggered effects
class PlainSilverTreasure(SilverTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.tag = ['no tag']
    
    # def getJsonObject(self):
    #     silverTreasureObject = {
    #         "silverTreasure": super().getJsonObject(),
    #         "tag": self.tag
    #     }
    #     return silverTreasureObject

# cards that have an activated ability after a dice is resolved to a specific value
class DiceEffectTreasure(SilverTreasure):
    def __init__(self, name, picture, eternal, diceCheck):
        super().__init__(name, picture, eternal)
        self.diceCheck = diceCheck
        self.tag = ['dice effect']

    def getDiceCheck(self):
        return self.diceCheck
    
    # def getJsonObject(self):
    #     diceEffectTreasureObject = {
    #         "silverTreasure": super().getJsonObject(),
    #         "tag": self.tag,
    #         "diceCheck": self.diceCheck
    #     }
    #     return diceEffectTreasureObject

# each time a player rolls a 2, recharge an item
class ChargedBaby(DiceEffectTreasure):
    def __init__(self, name, picture, eternal, diceCheck):
        super().__init__(name, picture, eternal, diceCheck)
        self.eternal = eternal
        self.name = name
        self.picture = picture
        self.diceCheck = diceCheck

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
        # silver items can't be recharged
        if isinstance(allItems.getCard(choice - 1), SilverTreasure):
            message = "Can't recharge a passive item"
            Json.systemOutput(message)
            return
        allItems.getCard(choice - 1).setTapped(False)
        message = f"{allItems.getCard(choice - 1).getName()} has been recharged"
        Json.systemOutput(message)
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
        message = "Choose a deck to look at the top card from"
        Json.choiceOutput(user.getSocketId(), message, ["Loot", "Monster", "Treasure"])
        choice = int(input())
        if choice == 1:
            # get a card from the loot deck and display the name to the player
            card = board.getLootDeck().deal()
            message = f"The loot card is {card.getName()}. Do you want to discard this card?"
            Json.choiceOutput(user.getSocketId(), message, ["Yes", "No"])
            cardDecision = int(input())
            if cardDecision == 1:
                # discard the card
                message = f"{card.getName()} has been discarded"
                Json.systemOutput(message)
                board.getDiscardLootDeck().addCardTop(card)
            elif cardDecision == 2:
                # put the card back on top of the deck
                message = f"{card.getName()} has been put back to the top of the deck"
                Json.systemOutput(message)
                board.getLootDeck().addCardTop(card)
        if choice == 2:
            # get a card from the monster deck and display the name to the player
            card = board.getMonsterDeck().deal()
            message = f"The monster card is {card.getName()}. Do you want to discard this card?"
            Json.choiceOutput(user.getSocketId(), message, ["Yes", "No"])
            cardDecision = int(input())
            if cardDecision == 1:
                # discard the card
                message = f"{card.getName()} has been discarded"
                Json.systemOutput(message)
                board.getDiscardMonsterDeck().addCardTop(card)
            elif cardDecision == 2:
                # put the card back on top of the deck
                message = f"{card.getName()} has been put back to the top of the deck"
                Json.systemOutput(message)
                board.getMonsterDeck().addCardTop(card)
        if choice == 3:
            # get a card from the treasure deck and display the name to the player
            card = board.getTreasureDeck().deal()
            message = f"The treasure card is {card.getName()}. Do you want to discard this card?"
            Json.choiceOutput(user.getSocketId(), message, ["Yes", "No"])
            cardDecision = int(input())
            if cardDecision == 1:
                # discard the card
                message = f"{card.getName()} has been discarded"
                Json.systemOutput(message)
                board.getDiscardTreasureDeck().addCardTop(card)
            elif cardDecision == 2:
                # put the card back on top of the deck
                message = f"{card.getName()} has been put back to the top of the deck"
                Json.systemOutput(message)
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
        # Shows players to select from
        message = "Choose a player to steal a loot card from their hand"
        playerChoice = user.getChosenPlayer(message, user)
        # show hand of that player
        message = "Choose a card from their hand to steal"
        playerOption = []
        for i in playerChoice.getHand().getCardList():
            playerOption.append(i.getName())
        Json.choiceOutput(user.getSocketId(), message, playerOption)
        cardChoice = int(input())
        # remove chosen card from chosen player and give it to user
        playerChoice.getHand().getCard(cardChoice - 1)
        playerChoice.getHand().removeCardIndex(cardChoice - 1)
        user.getHand().addCardTop(playerCard)
        message = f"Player {user.getNumber()} stole a loot card from Player {playerChoice}"
        Json.systemOutput(message)
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
        # ask if the player wants to use the finger
        message = "Do you want to use the finger?"
        Json.choiceOutput(user.getSocketId(), message, ["Yes", "No"])
        use = int(input())
        if use == 2:
            message = "chose to do nothing"
            Json.systemOutput(message)
            return
        # have to have more than 1 item to be able to swap, 1 because always have eternal item
        if room.getActivePlayer().getItems().getDeckLength() < 1 or user.getItems().getDeckLength() < 1:
            message = "Not enough items to swap"
            Json.systemOutput(message)
            return
        valid = False
        # loop to make sure they choose valid cards
        while valid is False:
            message = f"Choose which item from Player {room.getActivePlayer().getNumber()} to swap"
            playerOption = []
            for i in room.getActivePlayer().getItems().getCardList():
                playerOption.append(i.getName())
            Json.choiceOutput(user.getSocketId(), message, playerOption)
            cardChoice = int(input())
            # check to make sure selected card isn't an eternal item
            message = "Choose one of your items to swap"
            userOption = []
            for i in user.getItems.getCardList():
                userOption.append(i.getName())
            Json.choiceOutput(user.getSocketId(), message, userOption)
            userChoice = int(input())
            # check to make sure both chosen cards a not eternal, if they are break loop and go through it again
            if  room.getActivePlayer().getItems().getCard(cardChoice - 1).getEternal() == True:
                message = "Can't choose an eternal items from player to swap with"
                Json.systemOutput(message)
                break
            elif user.getItems().getCard(userChoice - 1).getEternal() == True:
                message = "Can't choose an eternal item from your items to swap with"
                Json.systemOutput(message)
                break
            else:
                message = f"Player {user.getNumber()} swapped his {user.getItems().getCard(userChoice - 1).getName()}"\
                      f"with Player's {room.getActivePlayer().getNumber()} "\
                      f"{room.getActivePlayer().getItems().getCard(cardChoice - 1).getName()}"
                Json.systemOutput(message)
                # have the user of finger, steal the card they wanted to swap from active player
                room.getBoard().stealTreasure(user, room.getActivePlayer(), cardChoice - 1)
                # have the active player steal user's chosen card that they wanted to swap with
                room.getBoard().stealTreasure(room.getActivePlayer(), user, userChoice - 1)
                return
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
        message = f"{user.getCharacter().getName()} just gained 1 loot from {self.name}!"
        Json.systemOutput(message)
        user.loot(1)
        # display all loot cards
        message = "Choose a card to discard"
        playerOption = []
        for i in user.getHand().getCardList():
            playerOption.append(i.getName())
        Json.choiceOutput(user.getSocketId(), message, playerOption)
        index = int(input()) - 1
        # discard a card
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
        message = f"Do you want to deal 1 damage to Player {stack[-1][1].getNumber()}"
        Json.choiceOutput(user.getSocketId(), message, ["Yes", "No"])
        choice = int(input())
        if choice == 1:
            # deal 1 damage to them
            stack[-1][1].getCharacter().takeDamage(1, user)
            message = f"Player {stack[-1][1].getNumber()} is cut by {self.name}!"
            Json.systemOutput(message)
        else:
            message = f"Player {stack[-1][1].getNumber()} is unaffected by {self.name}."
            Json.systemOutput(message)
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
        message = f"{user.getCharacter().getName()}'s greed yielded 3 cents."
        Json.systemOutput(message)
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
        message = f"{user.getCharacter().getName()} just gained 1 loot from {self.name}!"
        Json.systemOutput(message)
        user.loot(1)
        return

def createDiceEffectTreasures():
    diceEffectDeck = Deck([])
    charged_baby = ChargedBaby("Charged Baby", "test image.jpg", False, 2)
    diceEffectDeck.addCardTop(charged_baby)
    cheese_grater = CheeseGrater("Cheese Grater", "test image.jpg", False, 6)
    diceEffectDeck.addCardTop(cheese_grater)
    dead_bird = DeadBird("Dead Bird", "test image.jpg", False, 3)
    diceEffectDeck.addCardTop(dead_bird)
    eye_of_greed = EyeOfGreed("Eye Of Greed", "test image.jpg", False, 5)
    diceEffectDeck.addCardTop(eye_of_greed)
    finger = Finger("Finger", "test image.jpg", False, 2)
    diceEffectDeck.addCardTop(finger)
    moms_box = MomsBox("Mom's Box", "test image.jpg", False, 4)
    diceEffectDeck.addCardTop(moms_box)
    moms_razor = MomsRazor("Mom's Razor", "test image.jpg", False, 6)
    diceEffectDeck.addCardTop(moms_razor)
    the_relic = TheRelic("The Relic", "test image.jpg", False, 1)
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
            message = f"{self.name} creates riches (3c)!"
            Json.systemOutput(message)
            user.addCoins(3)
        elif count < 5:
            message = f"{self.name} conjures treasures (1 loot)!"
            Json.systemOutput(message)
            user.loot(1)
        else:
            user.takeDamage(1, user)
            message = f"{self.name} takes his payment (1 damage)!!"
            Json.systemOutput(message)
        return

# at start of your turn choose a player at random. that player destroys an item they control
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
            valid = False
            while valid is False:
                playerOption = []
                for i in chosenPlayer.getItems().getCardList():
                    playerOption.append(i.getName())
                message = f"Player {chosenPlayer.getNumber()}, which item will you destroy?"
                Json.choiceOutput(chosenPlayer.getSocketId(), message, playerOption)
                choice = int(input()) - 1
                # prevent player from choosing an eternal item
                if chosenPlayer.getItems().getCard(choice).getEternal() is True:
                    message = "Can't destroy an eternal item"
                    Json.systemOutput(message)
                else:
                    valid = True
            user.getBoard().discardTreasure(chosenPlayer, choice)
            message = f"Monstro destroys Player {chosenPlayer.getNumber()}'s {chosenItem.getName()}! :(("
            Json.systemOutput(message)
        # no items that can be destroyed
        else:
            message = f"Nothing for Monstro to destroy..."
            Json.systemOutput(message)
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
        playerOption = []
        message = f"There are {len(room.getBoard().getTreasures())} items in the shop. How many do you want to discard?"
        for i in range(len(room.getBoard().getTreasures())):
            playerOption.append(str(i + 1))
        Json.choiceOutput(user.getSocketId(), message, )
        choice = int(input())
        if choice > len(room.getBoard().getTreasures()):
            message = "Not enough items in shop to discard"
            Json.systemOutput(message)
            return
        else:
            # Iterate the amount of cards they want to discard and having them choose shop items to discard
            for i in range(choice):
                message = "Choose a shop item to discard"
                shopChoice = []
                for j in range(len(room.getBoard().getTreasures())):
                    shopChoice.append(room.getBoard().getTreasures()[j][-1].getName())
                Json.choiceOutput(user.getSocketId(), message, shopChoice)
                discardChoice = int(input())
                discardedCard = room.getBoard().getTreasure(discardChoice)
                room.getBoard().clearTreasureSlot(discardChoice)
                # add item card to discard pile
                room.getBoard().getDiscardTreasureDeck().addCardTop(discardedCard)
            # re-populate the shop
            room.getBoard().checkTreasureSlots()
        return


def createStartTurnTreasures():
    startTurnDeck = Deck([])
    dark_bum = DarkBum("Dark Bum", "test image.jpg", False)
    startTurnDeck.addCardTop(dark_bum)
    monstros_tooth = MonstrosTooth("Monstro's Tooth", "test image.jpg", False)
    startTurnDeck.addCardTop(monstros_tooth)
    restock = Restock("Restock", "test image.jpg", False)
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
            message = f"{user.getCharacter().getName()} just gained 6 cents from {self.name}!"
            Json.systemOutput(message)
            user.addCoins(6)
        else:
            message = f"{self.name} failed to activate..."
            Json.systemOutput(message)
        return

# at the end of your turn, you may discard any number of loot cards then loot equal to amount discarded this way
class GoatHead(EndTurnTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user):
        # Ask if the user wants to discard any of their cards
        message = f"Do you want to reroll any number of your loot cards?"
        Json.choiceOutput(user.getSocketId(), message, ["Yes", "No"])
        choice = int(input())
        #  if user want to discard
        if choice == 1:
            # ask for amount of cards they want to discard
            valueList = []
            for i in range(user.getHand().getDeckLength()):
                valueList.append(str(i + 1))
            message = "How many loot cards would you like to reroll?"
            Json.choiceOutput(user.getSocketId(), message, valueList)
            discardAmount = int(input())
            # loop until they discard based on amount they wanted to
            for i in range(discardAmount):
                user.chooseDiscard(0, user)
            # loot by amount of cards they discarded
            message = f"Player {user.getNumber()} sacrificed {discardAmount} loot cards and drew an equal amount."
            Json.systemOutput(message)
            user.loot(discardAmount)
        else:
            message = f"No sacrifices today ({self.name})."
            Json.systemOutput(message)
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
            message = f"{user.getCharacter().getName()} adds 2 loot cards to their collection ({self.name})!"
            Json.systemOutput(message)
            user.loot(2)
        else:
            message = f"{user.getCharacter().getName()} has a small collection of loot ({self.name})..."
            Json.systemOutput(message)
        return

# at end of turn look at top four cards of treasure deck and put them back in any order
class TheBlueMap(EndTurnTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user):
        message = f"Player {user.getName()} rearranges the Treasure Deck with {self.name}."
        Json.systemOutput(message)
        # use dummy deck to store order player wants cards put back
        dummyDeck = Deck([])
        room = user.getRoom()
        deck = user.drawTreasure(4)
        # put card in order that player wants them to be
        while deck.getDeckLength() > 0:
            deck.printCardListNames()
            index = int(input(f'Which card do you want to return to treasure deck: '))
            # CHOICE JSON
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
        message = f"Player {user.getNumber()} rearranges the Loot Deck with {self.name}."
        Json.systemOutput(message)
        # use dummy deck to store order player wants cards put back
        dummyDeck = Deck([])
        room = user.getRoom()
        deck = user.drawLoot(4)
        # put card in order that player wants them to be
        while deck.getDeckLength() > 0:
            deck.printCardListNames()
            index = int(input(f'Which card do you want to return to loot deck: '))
            # CHOICE JSON
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
        message = f"Player {user.getNumber()} rearranges the Monster Deck with {self.name}."
        Json.systemOutput(message)
        # use dummy deck to store order player wants cards put back
        dummyDeck = Deck([])
        room = user.getRoom()
        deck = user.drawMonster(4)
        # put card in order that player wants them to be
        while deck.getDeckLength() > 0:
            deck.printCardListNames()
            index = int(input(f'Which card do you want to return to monster deck: '))
            # CHOICE JSON
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
            message = f"{user.getCharacter().getName()} feels protected despite their circumstance, and finds 2 loot cards ({self.name})!"
            Json.systemOutput(message)
            user.loot(2)
        else:
            message = f"{user.getCharacter().getName()} grips their loot cards ({self.name})..."
            Json.systemOutput(message)
        return

def createEndTurnTreasures():
    endTurnDeck = Deck([])
    edens_blessing = EdensBlessing("Eden's Blessing", "test image.jpg", False)
    endTurnDeck.addCardTop(edens_blessing)
    goat_head = GoatHead("Goat Head", "test image.jpg", False)
    endTurnDeck.addCardTop(goat_head)
    starter_deck = StarterDeck("Starter Deck", "test image.jpg", False)
    endTurnDeck.addCardTop(starter_deck)
    the_blue_map = TheBlueMap("The Blue Map", "test image.jpg", False)
    endTurnDeck.addCardTop(the_blue_map)
    the_compass = TheCompass("The Compass", "test image.jpg", False)
    endTurnDeck.addCardTop(the_compass)
    the_map = TheMap("The Map", "test image.jpg", False)
    endTurnDeck.addCardTop(the_map)
    the_polaroid = ThePolaroid("The Polaroid", "test image.jpg", False)
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
            message = f"{self.name} has 6 or more counters! here is a treasure card."
            Json.systemOutput(message)
            user.gainTreasure(1)
            message = f"{self.name} now has {self.counter} counter(s) left."
            Json.systemOutput(message)
        else:
            message = f"{self.name} has {self.counter} counters."
            Json.systemOutput(message)
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
        message = f"Rolling for {self.name}..."
        Json.systemOutput(message)
        count = rollDice(user)
        # each other player takes 1 damage
        if count < 4:
            message = f"Filled with wrath you deal 1 damage to all other players!!"
            Json.systemOutput(message)
            for i in range(len(players)):
                if (i+1) != user.getNumber():
                    message = f"Player {i+1} is hurt by {self.name}!"
                    Json.systemOutput(message)
                    user.dealDamage(1, players[i])
        # deal 1 damage to a monster
        else:
            message = "Choose a monster to deal 1 damage to."
            monsterChoice = user.chooseMonster(message)
            message = f"{monsterChoice.getName()} is caught in Player {user.getNumber()}'s cursed blast, and takes 1 damage!"
            Json.systemOutput(message)
            user.dealDamage(1, monsterChoice)
        return

# each time you take damage loot 1
class FannyPack(TakeDamageTreasure):
    def __init__(self, name, picture, eternal):
        super().__init__(name, picture, eternal)
        self.eternal = eternal
        self.name = name
        self.picture = picture

    def use(self, user, damageNum):
        message = f"Ouch! Don't worry; loot a card ({self.name})."
        Json.systemOutput(message)
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