# Contributors: Jackson Cashman
# Contributors: Daniel De Guzman - getJsonObject()
"""
File defining the deck class
"""
import random
from Cards import *


class Deck:
    def __init__(self, cardList):
        self.cardList = cardList

    # getters

    # print the name of each card in the deck from index 0 --> -1
    def printCardListNames(self):
        # for i in range(len(self.cardList)):
        #    print(f"{i+1}: {self.cardList[i].getName()}")
        return

    def getDeckLength(self):
        return len(self.cardList)

    def getCardList(self):
        return self.cardList

    def getCard(self, index):
        if len(self.cardList) == 0:
            raise IndexError("Can't find a card from an empty deck!")
        if len(self.cardList) < index:
            raise IndexError("Index Error in getCard()")
        return self.cardList[index]

    def getCardName(self, name):
        for c in self.cardList:
            if c.getName() == name:
                return c

    def getJsonObject(self):
        if len(self.cardList) == 0:
            return []
        else:
            cardsJsonObjects = []
            for i in range(len(self.cardList)):
                cardsJsonObjects.append(self.cardList[i].getJsonObject())
            return cardsJsonObjects

    def getCardNamesAsJson(self):
        if len(self.cardList) == 0:
            return []
        else:
            cardNames = []
            for i in range(len(self.cardList)):
                cardNames.append(self.cardList[i].getName())
            return cardNames

    # other functions

    # deal a single card from the deck
    # that card is removed from the deck and returned
    def deal(self):
        if len(self.cardList) == 0:
            raise IndexError("Can't deal from an empty deck!")
        return self.cardList.pop(0)

    def shuffle(self):
        random.shuffle(self.cardList)
        return

    # adds a provided card to the top of the deck
    def addCardTop(self, card):
        self.cardList.insert(0, card)
        return

    # adds a provided card to the bottom of the deck
    def addCardBottom(self, card):
        self.cardList.append(card)
        return

    # adds a provided card to a specific index of the deck
    def addCardIndex(self, card, index):
        self.cardList.insert(index, card)
        return

    def combineDeck(self, deck2):
        self.cardList += deck2.getCardList()

    # remove a card with a index matching the input
    def removeCardIndex(self, index):
        removed = self.cardList[index]
        self.cardList.remove(self.cardList[index])
        return removed

    # remove a card with a name matching the input
    def removeCardName(self, name):
        for c in self.cardList:
            if c.getName() == name:
                removed = c
                self.cardList.remove(removed)
        return removed
