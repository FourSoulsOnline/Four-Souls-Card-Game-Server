# Contributors: Jackson Cashman
'''
File containing the creation of Enemy cards
'''

from Decks import Deck
from Cards import Enemy
from Cards import Entity
from Cards import GoldTreasure
from Coins import *
from LootReward import *
from TreasureReward import TreasureReward
from Player import Player
from Dice import Dice
from Dice import rollDice
from JsonOutputHelper import JsonOutputHelper
import random
Json = JsonOutputHelper()

def lootX(attacker):
    # loot X cards
    message = f"Player {attacker.getNumber()} rolls for loot reward..."
    Json.systemOutput(message)
    count = rollDice(attacker)
    attacker.loot(count)
    return count

def coinX(attacker):
    # gain X coins
    message = f"Player {attacker.getNumber()} rolls for coin reward..."
    Json.systemOutput(message)
    count = rollDice(attacker)
    attacker.addCoins(count)
    return count

def createBasicEnemyCards():
    # Here are all enemies that lack any special effects
    # name, picture, maxHp, attack, diceValue, soulCount, reward
    basicEnemyDeck = Deck([])
    clotty = Enemy("Clotty", "test image.jpg", 2, 1, 3, 0, [CoinStack(4)])
    basicEnemyDeck.addCardTop(clotty)
    cod_worm = Enemy("Cod Worm", "test image.jpg", 2, 0, 5, 0, [CoinStack(3)])
    basicEnemyDeck.addCardTop(cod_worm)
    conjoined_fatty = Enemy("Conjoined Fatty", "test image.jpg", 4, 2, 3, 0, [LootReward(2)])
    basicEnemyDeck.addCardTop(conjoined_fatty)
    dip = Enemy("Dip", "test image.jpg", 1, 1, 4, 0, [CoinStack(1)])
    basicEnemyDeck.addCardTop(dip)
    fat_bat = Enemy("Fat Bat", "test image.jpg", 3, 1, 5, 0, [TreasureReward(1)])
    basicEnemyDeck.addCardTop(fat_bat)
    fatty = Enemy("Fatty", "test image.jpg", 4, 1, 2, 0, [LootReward(1)])
    basicEnemyDeck.addCardTop(fatty)
    fly = Enemy("Fly", "test image.jpg", 1, 1, 2, 0, [CoinStack(1)])
    basicEnemyDeck.addCardTop(fly)
    leech = Enemy("Leech", "test image.jpg", 1, 2, 4, 0, [LootReward(1)])
    basicEnemyDeck.addCardTop(leech)
    pale_fatty = Enemy("Pale Fatty", "test image.jpg", 4, 1, 3, 0, [CoinStack(6)])
    basicEnemyDeck.addCardTop(pale_fatty)
    pooter = Enemy("Pooter", "test image.jpg", 2, 1, 3, 0, [LootReward(1)])
    basicEnemyDeck.addCardTop(pooter)
    red_host = Enemy("Red Host", "test image.jpg", 2, 2, 3, 0, [CoinStack(5)])
    basicEnemyDeck.addCardTop(red_host)
    spider = Enemy("Spider", "test image.jpg", 1, 1, 4, 0, [LootReward(1)])
    basicEnemyDeck.addCardTop(spider)
    squirt = Enemy("Squirt", "test image.jpg", 2, 1, 3, 0, [LootReward(1)])
    basicEnemyDeck.addCardTop(squirt)
    trite = Enemy("Trite", "test image.jpg", 1, 1, 5, 0, [LootReward(2)])
    basicEnemyDeck.addCardTop(trite)
    return basicEnemyDeck

def createBasicBossCards():
    # Here are all bosses that lack any special effects
    # name, picture, maxHp, attack, maxAttack, diceValue, soulCount, reward
    basicBossDeck = Deck([])
    gurdy = Enemy("Gurdy", "test image.jpg", 5, 1, 4, 1, [CoinStack(7)])
    basicBossDeck.addCardTop(gurdy)
    little_horn = Enemy("Little Horn", "test image.jpg", 2, 1, 6, 1, [LootReward(2)])
    basicBossDeck.addCardTop(little_horn)
    monstro = Enemy("Monstro", "test image.jpg", 4, 1, 4, 1, [CoinStack(6)])
    basicBossDeck.addCardTop(monstro)
    return basicBossDeck

# when this dies, the active player may attack the monster deck an additional time (BIG SPIDER)
class monsterDieExtraAttack(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def dieEffect(self, attacker):
        message = f"Player {attacker.getRoom().getActivePlayerIndex() + 1} can attack an additional time this turn ({self.name})."
        Json.systemOutput(message)
        attacker.getCharacter().addAttacksLeft()
        return

# when this dies, it deals 1 damage to the player who killed it (BLACK BONY)
class monsterDieRevengeDamage(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def dieEffect(self, attacker):
        # get active player
        activePlayer = attacker.getRoom().getActivePlayer()
        # loot X cards
        lootX(activePlayer)
        # deal 1 damage to that player
        message = f"{self.name} explodes, dealing 1 damage to Player {attacker.getNumber()}."
        Json.systemOutput(message)
        attacker.takeDamage(1, self)
        return

# when this dies, it deals 1 damage to each player (BOOM FLY)
class monsterDieDamageAllPlayers(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    # TODO: im pretty sure this will throw an error if a non player kills this
    def dieEffect(self, attacker):
        playerList = attacker.getRoom().getPlayers()
        message = f"{self.name} explodes, dealing 1 damage to all players!"
        Json.systemOutput(message)
        for i in range(len(playerList)):
            # deal damage to each player in turn order, starting with the active player
            playerList[(attacker.getNumber() - 1 + i) % len(playerList)].takeDamage(1, self)
        return

# when this dies, the active player forces a player to discard 2 loot cards (DANK GLOBIN)
class monsterDieChooseDiscard(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward, num):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp
        # num is the number of loot cards that the chosen player will discard
        self.num = num

    def dieEffect(self, attacker):
        # choose a player to discard
        attacker.getRoom().displayCharacters()
        message = "Force which player to discard 2 loot cards? >:)"
        chosenPlayer = activePlayer.getChosenPlayer(message, activePlayer)
        # discard 2 loot cards
        message = f"Player {attacker.getRoom().getActivePlayerIndex+1} forces Player {playerIndex} to discard 2 loot cards ({self.name})!"
        Json.systemOutput(message)
        for i in range(self.num):
            # show loot cards in hand
            chosenPlayer.getHand().printCardListNames()
            # remove the card
            chosenPlayer.chooseDiscard(1, chosenPlayer)
        return

# when this dies on an attack roll of 6, double its rewards (DINGA)
class monsterDieDinga(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp
        # num is the dice value being compared
        num = 6

    def dieEffect(self, attacker):
        # choose a player to discard
        room = attacker.getRoom()
        stack = room.getStack()
        doubled = False
        # check if stack element above this is a dice result 6
        try:
            if isinstance(stack.getLastResolved()[0], Dice):
                if stack.getLastResolved()[0].getResult() == 6:
                    doubled = True
        except:
            pass
        # identify active player
        activePlayer = room.getActivePlayer()
        # gain x cents (possibly doubled)
        count = coinX(activePlayer)
        if doubled == True:
            message = f"{self.name} dies on an attack roll of 6. Player {attacker.getRoom().getActivePlayerIndex+1} gains doubled rewards!"
            Json.systemOutput(message)
            activePlayer.addCoins(count)
        return

# damage dealt to this is also dealt to the player to the active player's left/right (DOPLE/EVIL TWIN)
class monsterHurtSplash(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward, lr):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp
        # lr defines if splash damage goes left or right
        self.lr = lr

    # Entity will take num damage
    # Entity hp cannot go below 0
    # attacker is another entity
    def takeDamage(self, num, attacker):
        # Look through character being attacked inventory to check for ReduceDamage effect
        if len(self.inventory) != 0:
            for i in range(len(self.inventory)):
                if isinstance(self.inventory[len(self.inventory) - i - 1], ReduceDamage):
                    num = self.inventory[len(self.inventory) - i - 1].effect(num)
                    self.clearEffect(len(self.inventory) - i - 1)
        # this takes damage
        self.hp -= num
        if self.hp <= 0:
            self.die(attacker)
        # find the active player
        activePlayerIndex = attacker.getRoom().getActivePlayerIndex()
        players = attacker.getRoom().getPlayers()
        # deal damage to left/right player
        if self.lr == "left":
            message = f"Player {(activePlayerIndex - 1) % 4} receives {num} splash damage from Player {attacker.getNumber()}'s attack!"
            Json.systemOutput(message)
            leftPlayer = players[(activePlayerIndex - 1) % 4]
            leftPlayer.takeDamage(num, attacker)
        elif self.lr == "right":
            message = f"Player {(activePlayerIndex + 1) % 4} receives {num} splash damage from Player {attacker.getNumber()}'s attack!"
            Json.systemOutput(message)
            rightPlayer = players[(activePlayerIndex + 1) % 4]
            rightPlayer.takeDamage(num, attacker)
        else:
            raise ValueError("'lr' must be filled as either 'left' or 'right'")
        return

# when this dies the active player chooses a player, they lose 7 cents (GREEDLING)
class monsterDieGreedling(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def dieEffect(self, attacker):
        # choose a player to discard
        attacker.getRoom().displayCharacters()
        message = "Force which player to lose 7 cents? >:)"
        chosenPlayer = activePlayer.getChosenPlayer(message, activePlayer)
        # lose 7c
        message = f"Player {attacker.getRoom().getActivePlayerIndex+1} steals 7 cents from Player {playerIndex} ({self.name})!"
        Json.systemOutput(message)
        chosenPlayer.subtractCoins(7)
        return

# when this dies expand shop slots by 1 (HANGER)
class monsterDieExpandShop(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward, slots):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp
        self.slots = slots

    def dieEffect(self, attacker):
        message = f"{self.name} reveals 2 new shop slots."
        Json.systemOutput(message)
        for i in range(self.slots):
            attacker.getRoom().getBoard().addTreasureSlot()
            attacker.getRoom().getBoard().checkTreasureSlots()
        return

# this takes no damage on attack rolls of 6 (HOPPER)
class monsterRollImmunity(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward, val):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp
        self.val = val # val is the one dice roll that the monster is impervious to

    def takeDamage(self, num, attacker):
        # if the stack element above this monster is a dice and it is a 6
        if len(attacker.getRoom().getStack().getStack()) == 1:
            if isinstance(attacker.getRoom().getStack().getLastResolved()[0], Dice):
                result = attacker.getRoom().getStack().getLastResolved()[0].getResult()
                if result == 6:
                    # return without dealing damage
                    message = f"{self.name} evades damage on attack rolls of 6. :("
                    Json.systemOutput(message)
                    return
        # take damage as normal
        Entity.takeDamage(self, num, attacker)
        return

# combat damage this deals in increased by 1 on attack rolls of 1 (HORF)
class monsterRollHorf(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def dealDamage(self, num, target):
        atk = self.attack
        # if index 1 on the stack is a dice roll and a 2
        if len(target.getRoom().getStack().getStack()) == 1:
            if isinstance(target.getRoom().getStack().getLastResolved()[0], Dice):
                result = target.getRoom().getStack().getLastResolved()[0].getResult()
                if result == 2:
                    # increase attack by 1
                    self.setAttack(atk + 1)
                    message = f"{self.name} deals bonus damage this turn!"
                    Json.systemOutput(message)
        Entity.dealDamage(self, self.attack, target)
        # return attack to normal
        self.setAttack(atk)
        return

# combat damage this deals is doubled on attack rolls of 1 (LEAPER)
class monsterRollLeaper(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def dealDamage(self, num, target):
        atk = self.attack
        # if index 1 on the stack is a dice roll and a 2
        if len(attacker.getRoom().getStack().getStack()) == 1:
            if isinstance(target.getRoom().getStack().getLastResolved()[0], Dice):
                result = target.getRoom().getStack().getLastResolved()[0].getResult()
                if result == 1:
                    # double attack
                    self.setAttack(atk + atk)
                    message = f"{self.name} deals bonus damage on attack rolls of 1!"
                    Json.systemOutput(message)
        Entity.dealDamage(self, self.attack, target)
        # return attack to normal
        self.setAttack(atk)
        return

# each time this deals combat damage to a player, they lose 2c (KEEPER HEAD)
class monsterDamageKeeperHead(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def damageEffect(self, target):
        message = f"{self.name} steals two of Player {target.getNumber()}'s coins!"
        Json.systemOutput(message)
        target.subtractCoins(2)
        return

    def dieEffect(self, attacker):
        # get active player
        activePlayer = attacker.getRoom().getActivePlayer()
        # gain X coins
        coinX(activePlayer)
        return

# when this dies, the active player may steal a non eternal item another player controls (MOM'S DEAD HAND)
# TODO: eternal items can be stolen currently
class monsterDieMomsDeadHand(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def dieEffect(self, attacker):
        # get room
        room = attacker.getRoom()
        # get active player
        activePlayer = room.getActivePlayer()
        # choose a player
        room.displayCharacters()
        activePlayer.chooseItemSteal()
        return

# when this dies, the active player deals 3 damage to a player (MULLIBOOM)
class monsterDieMulliboom(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def dieEffect(self, attacker):
        # get room
        room = attacker.getRoom()
        # get active player
        activePlayer = room.getActivePlayer()
        # choose a player
        room.displayCharacters()
        message = "Deal 3 damage to which player?"
        chosenPlayer = activePlayer.chooseAnyPlayer(message)
        message = f"Player {activePlayer.getNumber()} blows up {self.name} next to Player {num+1}!!"
        Json.systemOutput(message)
        activePlayer.dealDamage(3, chosenPlayer)
        return

# when this dies, expand monster slots by 1 (MULLIGAN)
class monsterDieMulligan(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def dieEffect(self, attacker):
        # get board
        board = attacker.getRoom().getBoard()
        board.addMonsterSlot()
        message = f"More monsters appeared! ({self.name})"
        Json.systemOutput(message)
        return

# when this dies, the active player recharges each item they control (PSY HORF)
class monsterDiePsyHorf(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def dieEffect(self, attacker):
        # get room
        room = attacker.getRoom()
        # get active player
        activePlayer = room.getActivePlayer()
        itemDeck = activePlayer.getItems()
        message = f"Player {activePlayer.getNumber()} uses {self.name}'s psychic power to recharge all their items."
        Json.systemOutput(message)
        for i in range(itemDeck.getDeckLength()):
            if isinstance(activePlayer.getItems().getCardList()[i], GoldTreasure):
                activePlayer.getItems().getCardList()[i].setTapped(False)
        return

# damage this deals to the active player is also dealt to the player to their left (RAGE CREEP)
class monsterDamageRageCreep(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def damageEffect(self, target):
        if target == target.getRoom().getActivePlayer():
            activeNum = target.getRoom().getActivePlayer().getNumber()
            numPlayers = len(target.getRoom().getPlayers())
            leftPlayer = target.getRoom().getPlayers()[activeNum % numPlayers]
            message = f"{self.name} attacks to the left. Player {leftPlayer.getNumber()} is caught in the crossfire!"
            Json.systemOutput(message)
            self.dealDamage(self.attack, leftPlayer)
        return

# when this dies, the active player must make an additional attack (PORTAL)
class monsterDieExtraMandatoryAttack(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def dieEffect(self, attacker):
        # get room
        room = attacker.getRoom()
        # get active player
        activePlayer = room.getActivePlayer()
        activePlayer.getCharacter().addMandatoryAttacks()
        message = f"Player {activePlayer.getNumber()} must attack again this turn ({self.name})!"
        Json.systemOutput(message)
        return

# each time the attacking player rolls and attack roll of 3, they must steal a loot card from another player at random (RING OF FLIES)
class monsterRollRingOfFlies(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    # steals a random loot card from another player with loot cards
    def stealLoot(self, player):
        # get room
        room = player.getRoom()
        # get players
        players = room.getPlayers()
        # get active player
        activePlayer = room.getActivePlayer()
        numPlayers = len(player.getRoom().getPlayers())
        viableHands = [] # list with the player number of players with at least 1 loot card in hand (exclusing active player)
        # determine which players have loot cards
        for i in range(numPlayers):
            # cant steal from empty hand
            if players[i].getHand().getDeckLength() <= 0:
                continue
            # active player cant steal from self
            if players[i] == activePlayer:
                continue
            viableHands.append(players[i].getNumber())
        if len(viableHands) == 0:
            message = f"No loot cards to steal ({self.name})."
            Json.systemOutput(message)
            return
        chosenNum = random.choice(viableHands) # the player number who will be stolen from
        chosenHandLen = players[chosenNum -1].getHand().getDeckLength()
        chosenIndex = random.randint(1, chosenHandLen) - 1 # the index of the card to be stolen
        stolenLoot = players[chosenNum - 1].getHand().removeCardIndex(chosenIndex)
        activePlayer.getHand().addCardBottom(stolenLoot)
        message = f"Player {activePlayer.getNumber()} stole a loot card from Player {chosenNum} ({self.name})!"
        Json.systemOutput(message)
        return

    def takeDamage(self, num, attacker):
        # make attacking player steal a loot if they rolled a 3
        if len(attacker.getRoom().getStack().getStack()) == 1:
            if isinstance(attacker.getRoom().getStack().getLastResolved()[0], Dice):
                if attacker.getRoom().getStack().getLastResolved()[0].getResult() == 3:
                    self.stealLoot(attacker)
        # take damage after stealing loot
        Entity.takeDamage(self, num, attacker)
        return

    def dealDamage(self, num, target):
        # make attacking player steal a loot if they rolled a 3
        if len(attacker.getRoom().getStack().getStack()) == 1:
            if isinstance(target.getRoom().getStack().getLastResolved()[0], Dice):
                if target.getRoom().getStack().getLastResolved()[0].getResult() == 3:
                    self.stealLoot(target)
        # deal damage after stealing loot
        Entity.dealDamage(self, num, target)
        return

# each time the attacking player rolls and attack roll of 5, they take 1 damage (SWARM OF FLIES)
class monsterRollSwarmOfFlies(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def takeDamage(self, num, attacker):
        # make attacking player steal a loot if they rolled a 3
        if len(attacker.getRoom().getStack().getStack()) == 1:
            if isinstance(attacker.getRoom().getStack().getLastResolved()[0], Dice):
                if attacker.getRoom().getStack().getLastResolved()[0].getResult() == 5:
                    message = f"{self.name} deals 1 damage (attack roll of 5)!"
                    Json.systemOutput(message)
                    attacker.takeDamage(1, self)
        # take damage after stealing loot
        Entity.takeDamage(self, num, attacker)
        return

    def dealDamage(self, num, target):
        # make attacking player steal a loot if they rolled a 3
        if len(attacker.getRoom().getStack().getStack()) == 1:
            if isinstance(target.getRoom().getStack().getLastResolved()[0], Dice):
                if target.getRoom().getStack().getLastResolved()[0].getResult() == 5:
                    message = f"{self.name} deals 1 damage (attack roll of 5)!"
                    Json.systemOutput(message)
                    attacker.takeDamage(1, self)
        # deal damage after stealing loot
        Entity.dealDamage(self, num, target)
        return

# when this dies, the active player chooses a player. that player destroys a soul card (WIZOOB)
# TODO: will need to be edited when souls are reworked
class monsterDieDestroySoul(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def dieEffect(self, attacker):
        # get room
        room = attacker.getRoom()
        # get active player
        activePlayer = room.getActivePlayer()
        # choose a player
        room.displayCharacters()
        message = "Force which player to destroy a soul?"
        chosenPlayer = activePlayer.chooseAnyPlayer(message)
        if chosenPlayer.getSouls() >= 1:
            chosenPlayer.subtractSouls(1)
            message = f"Player {chosenPlayer.getNumber()} was forced to lose a soul by Player {activePlayer.getNumber()} ({self.name})!"
            Json.systemOutput(message)
        else:
            message = f"Player {chosenPlayer.getNumber()} had no souls to discard ({self.name})!"
            Json.systemOutput(message)
        return

# this takes no damage on attack rolls of 4 or 5 (CARRION QUEEN)
class monsterRollCarrionQueen(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def takeDamage(self, num, attacker):
        # if the stack element above this monster is a dice and it is a 4 or 5
        if len(attacker.getRoom().getStack().getStack()) == 1:
            if isinstance(attacker.getRoom().getStack().getLastResolved()[0], Dice):
                result = attacker.getRoom().getStack().getLastResolved()[0].getResult()
                if (result == 4) or (result == 5):
                    # return without dealing damage
                    message = f"{self.name} is immune to damage rolls of 4 and 5! DD:"
                    Json.systemOutput(message)
                    return
        # take damage as normal
        Entity.takeDamage(self, num, attacker)
        return

# when this dies, the active player chooses a player. that player gives you a soul (THE LAMB)
class monsterDieStealSoul(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def dieEffect(self, attacker):
        # get room
        room = attacker.getRoom()
        # get board
        board = attacker.getRoom().getBoard()
        # get active player
        activePlayer = room.getActivePlayer()
        # choose a player
        room.displayCharacters()
        message = "Force which player to give you a soul?"
        chosenPlayer = activePlayer.getChosenPlayer(message, activePlayer)
        if chosenPlayer.getSouls() >= 1:
            chosenPlayer.subtractSouls(1)
            activePlayer.addSouls(1)
            message = f"Player {chosenPlayer.getNumber()} was forced to give a soul to Player {activePlayer.getNumber()} ({self.name})!"
            Json.systemOutput(message)
        else:
            message = f"Player {chosenPlayer.getNumber()} had no souls for Player {activePlayer.getNumber()} to steal ({self.name})!"
            Json.systemOutput(message)
        return

# when this dies, the active player chooses a player. that player dies (DEATH)
class monsterDieKillPlayer(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def dieEffect(self, attacker):
        # get room
        room = attacker.getRoom()
        # get active player
        activePlayer = room.getActivePlayer()
        # choose a player
        room.displayCharacters()
        # kill
        message = f"Kill which player ({self.name})?"
        chosenPlayer = attacker.chooseAnyPlayer(message)
        if chosenPlayer.getHp() > 0:
            chosenPlayer.die(activePlayer)
            message = f"Player {activePlayer.getNumber()} kills Player {chosenPlayer.getNumber()} ({self.name})!"
            Json.systemOutput(message)
        return

# when this is at 1 hp it has +1 attack (Gemini)
class monsterHpGemini(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def dealDamage(self, num, target):
        targetHp = target.getHp()
        if self.hp == 1:
            num += 1
            message = f"{self.name} dealt 1 bonus damage!"
            Json.systemOutput(message)
        target.takeDamage(num, self)
        # make sure that damage was not prevented before carrying out damage procs
        if target.getHp() < targetHp:
            self.damageEffect(target)
        return

# each time this takes damage on an attack roll of 6 deal 1 damage to the player to the active players left (GLUTTONY)
class monsterRollGluttony(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def takeDamage(self, num, attacker):
        Entity.takeDamage(self, num, attacker)
        # check for a roll of 6
        if len(attacker.getRoom().getStack().getStack()) == 1:
            if isinstance(attacker.getRoom().getStack().getLastResolved()[0], Dice):
                if attacker.getRoom().getStack().getLastResolved()[0].getResult() == 6:
                    # deal damage to left player
                    # find the active player
                    activePlayerIndex = attacker.getRoom().getActivePlayerIndex()
                    players = attacker.getRoom().getPlayers()
                    # deal damage to left/right player
                    leftPlayer = players[(activePlayerIndex - 1) % 4]
                    message = f"Player {leftPlayer.getNumber()} is hurt by {self.name}'s splash damage!"
                    Json.systemOutput(message)
                    leftPlayer.takeDamage(1, self)
        return

class monsterDamageGreed(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def damageEffect(self, target):
        message = f"{self.name} makes everyone drop 4 pennies!"
        Json.systemOutput(message)
        for i in range(len(target.getRoom().getPlayers())):
            target.getRoom().getPlayers()[i].subtractCoins(4)
        return

# each time this takes damage it gains +1 attack till end of turn
class monsterHurtDamageUp(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def takeDamage(self, num, attacker):
        Entity.takeDamage(self, num, attacker)
        message = f"{self.name}'s rage grows... (+1 ATK)"
        Json.systemOutput(message)
        self.attack += 1
        return

# when this is at 2 hp or less it has +1 dice (LARRY JR.)
class monsterHpLarryJr(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def takeDamage(self, num, attacker):
        # check that larry jr is in the appropriate hp range
        if self.hp <= 2:
            # the only things on the stack are declared attack and dice roll
            if len(attacker.getRoom().getStack().getStack()) == 1:
                if isinstance(attacker.getRoom().getStack().getLastResolved()[0], Dice):
                    # if they rolled exactly enough to hurt larry jr without the dice buff
                    if attacker.getRoom().getStack().getLastResolved[0].getResult() <= self.diceValue:
                        if self.diceValue != 6: # if larry jr somehow gets 6 dice it still needs to be possible to hurt it
                            message = f"{self.name} evades the attack!"
                            Json.systemOutput(message)
                            self.dealDamage(self.attack, attacker)
                            return
        Entity.takeDamage(self, num, attacker)
        return

# each time this takes combat damage it deals 1 damage to the attacking player (LUST)
class monsterHurtLust(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def takeDamage(self, num, attacker):
        hp = self.hp
        Entity.takeDamage(self, num, attacker)
        # make sure damage was a combat roll
        if len(attacker.getRoom().getStack().getStack()) == 1:
            if isinstance(attacker.getRoom().getStack().getLastResolved()[0], Dice):
                if self.hp < hp: # if damage was actually dealt
                    # deal 1 thorns damage
                    message = f"{self.name} tries to take Player {attacker.getNumber()} down with itself...!"
                    Json.systemOutput(message)
                    self.dealDamage(1, attacker)
        return

# when this is at 1 hp it has +2 dice (MASK OF INFAMY)
class monsterHpMaskOfInfamy(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def takeDamage(self, num, attacker):
        # check that mask is in the appropriate hp range
        if self.hp == 1:
            # the only things on the stack are declared attack and dice roll
            if len(attacker.getRoom().getStack().getStack()) == 1:
                if isinstance(attacker.getRoom().getStack().getLastResolved()[0], Dice):
                    # if they rolled exactly to hurt mask without the dice buff
                    if attacker.getRoom().getStack().getLastResolved()[0].getResult() <= (self.diceValue + 1):
                        if self.diceValue != 6: # if mask somehow gets 6 dice it still needs to be possible to hurt it
                            message = f"{self.name} evades the attack!"
                            Json.systemOutput(message)
                            self.dealDamage(self.attack, attacker)
                            return
        Entity.takeDamage(self, num, attacker)
        return

# each time this deals combat damage, it heals 1 hp (MEGA FATTY)
class monsterDamageMegaFatty(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def damageEffect(self, target):
        if self.hp < self.maxHp:
            message = f"{self.name} takes time to eat its leftovers."
            Json.systemOutput(message)
            self.hp += 1
        return

# each time this deals combat damage to a player, the player discards 1 loot card (SCOLEX)
class monsterDamageScolex(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def damageEffect(self, target):
        if target.getHand().getDeckLength() > 0:
            message = f"{self.name} knocks a loot card out of your hand."
            Json.systemOutput(message)
            target.getHand().printCardListNames()
            target.chooseDiscard(1, target)
        return

# when this dies, the player that killed it discards their hand (SLOTH)
class monsterDieSloth(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def dieEffect(self, attacker):
        # get room
        room = attacker.getRoom()
        # get board
        board = attacker.getRoom().getBoard()
        # discard hand
        for i in range(attacker.getHand().getDeckLength()):
            discard = attacker.getHand().removeCardIndex(0)
            attacker.getRoom().getBoard().getDiscardLootDeck().addCardTop(discard)
        message = f"All of your loot cards turn to dust!?"
        Json.systemOutput(message)
        return

# each time this deals combat damage it deals 1 damage to all other players (THE BLOAT)
class monsterDamageTheBloat(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def damageEffect(self, target):
        activePlayer = target.getRoom().getActivePlayer()
        # no effect occurs if a non active player is damaged
        if target is not activePlayer:
            return
        players = target.getRoom().getPlayers()
        for i in range(len(players)):
            if players[i] is not activePlayer:
                # deal 1 damage to each non active player
                self.dealDamage(1, players[i])
        message = f"Everyone is caught in {self.name}'s crossfire!!"
        Json.systemOutput(message)
        return

# each time this would take damage the active player rolls. on 1 prevent that damage (THE DUKE OF FLIES)
class monsterHurtTheDukeOfFlies(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def takeDamage(self, num, attacker):
        # roll a dice
        message = f"Roll for {self.name}..."
        Json.systemOutput(message)
        count = rollDice(attacker)
        # take no damage on a roll of 1
        if count == 1:
            message = f"A stray fly blocks Player {attacker.getNumber()}'s attack..."
            Json.systemOutput(message)
            return
        Entity.takeDamage(self, num, attacker)
        return

# when this dies, the active player deals 2 damage divded as they choose to any number of players or monsters (PESTILENCE)
class monsterDiePestilence(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def dieEffect(self, attacker):
        # get room
        room = attacker.getRoom()
        playerList = room.getPlayers()
        # get active player
        activePlayer = room.getActivePlayer()
        # deal 1 damage twice
        for i in range(2):
            message = f"Deal 1 damage to which creature?"
            chosenEntity = attacker.chooseAnyEntity(message)
            message = f"Player {activePlayer.getNumber()} did 1 damage to " \
                      f"{chosenEntity.getName()} ({self.name})!"
            Json.systemOutput(message)
            chosenEntity.takeDamage(1, activePlayer)
        return

# when this dies, the active player rolls. 1-3 all players take 1 damage. 4-6 all players take 2 damage (WRATH)
class monsterDieWrath(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def dieEffect(self, attacker):
        # get room
        room = attacker.getRoom()
        playerList = room.getPlayers()
        # roll a dice
        message = f"Rolling for {self.name}...!"
        Json.systemOutput(message)
        count = rollDice(attacker)
        if count < 4:
            message = f"Everyone is caught in {self.name}'s explosion!"
            Json.systemOutput(message)
            for i in range(len(playerList)):
                self.dealDamage(1, playerList[i])
        else:
            message = f"Everyone is caught in {self.name}'s inferno!!"
            Json.systemOutput(message)
            for i in range(len(playerList)):
                self.dealDamage(2, playerList[i])
        return

# combat damage this deals is doubled on attack rolls of 1. when this dies expand monster slots by 1 (MOM!)
class monsterRollDieMom(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def dealDamage(self, num, target):
        atk = self.attack
        # if index 1 on the stack is a dice roll and a 1
        if len(target.getRoom().getStack().getStack()) == 1:
            if isinstance(target.getRoom().getStack().getLastResolved()[0], Dice):
                result = target.getRoom().getStack().getLastResolved()[0].getResult()
                if result == 1:
                    # double attack
                    self.setAttack(atk + atk)
                    message = f"{self.name} deals {atk} + {atk} damage this roll!"
                    Json.systemOutput(message)
        Entity.dealDamage(self, self.attack, target)
        # return attack to normal
        self.setAttack(atk)
        return

    def dieEffect(self, attacker):
        # get board
        board = attacker.getRoom().getBoard()
        board.addMonsterSlot()
        message = f"More monsters appeared ({self.name})!"
        Json.systemOutput(message)
        return

# each time the attacking player rolls an attack roll of 6 they choose a living player, that player dies (SATAN)
class monsterRollSatan(Enemy):
    def __init__(self, name, picture, maxHp, attack, diceValue, soulCount, reward):
        super().__init__(name, picture, maxHp, attack, diceValue, soulCount, reward)
        self.hp = maxHp

    def takeDamage(self, num, attacker):
        room = attacker.getRoom()
        activePlayer = room.getActivePlayer()
        # the only things on the stack are declared attack and dice roll
        #if len(attacker.getRoom().getStack().getStack()) == 2:
        if len(attacker.getRoom().getStack().getStack()) == 1:
            if isinstance(attacker.getRoom().getStack().getLastResolved()[0], Dice):
            #if isinstance(attacker.getRoom().getStack().getStack()[1][0], Dice):
                # if they rolled exactly 6
                #if attacker.getRoom().getStack().getStack()[1][0].getResult() == 6:
                if attacker.getRoom().getStack().getLastResolved()[0].getResult() == 6:
                    message = f"Player {activePlayer.getNumber()} makes a deal with the devil..."
                    Json.systemOutput(message)
                    # choose a player
                    room.displayCharacters()
                    # kill
                    kill = False
                    tries = 0
                    while kill == False:
                        message = f"Kill which living player ({self.name})?"
                        chosenPlayer = attacker.chooseAnyPlayer(message)
                        # kill the chosen player (if they are alive)
                        if chosenPlayer.getHp() > 0:
                            chosenPlayer.die(activePlayer)
                            message = f"Player {activePlayer.getNumber()} kills Player {chosenPlayer.getNumber()} ({self.name})!"
                            Json.systemOutput(message)
                            kill = True
                        tries += 1
                        # this should prevent a softlock when all players are dead
                        if tries == len(room.getPlayers()):
                            return
        Entity.takeDamage(self, num, attacker)
        return

def createAdditionalEnemeies():
    # name, picture, maxHp, attack, diceValue, soulCount, reward
    additionalEnemyDeck = Deck([])
    big_spider = monsterDieExtraAttack("Big Spider", "test image.jpg", 3, 1, 4, 0, [LootReward(1)])
    additionalEnemyDeck.addCardTop(big_spider)
    boom_fly = monsterDieDamageAllPlayers("Boom Fly", "test image.jpg", 1, 1, 4, 0, [CoinStack(4)])
    additionalEnemyDeck.addCardTop(boom_fly)
    black_bony = monsterDieRevengeDamage("Black Bony", "test image.jpg", 3, 1, 4, 0, [LootXReward()])
    additionalEnemyDeck.addCardTop(black_bony)
    dank_globin = monsterDieChooseDiscard("Dank Goblin", "test image.jpg", 2, 2, 4, 0, [LootReward(2)], 2)
    additionalEnemyDeck.addCardTop(dank_globin)
    dinga = monsterDieDinga("Dinga", "test image.jpg", 3, 1, 3, 0, [CoinXReward()])
    additionalEnemyDeck.addCardTop(dinga)
    dople = monsterHurtSplash("Dople", "test image.jpg", 2, 2, 4, 0, [CoinStack(7)], "right")
    additionalEnemyDeck.addCardTop(dople)
    evil_twin = monsterHurtSplash("Evil Twin", "test image.jpg", 3, 2, 5, 0, [TreasureReward(1)], "left")
    additionalEnemyDeck.addCardTop(evil_twin)
    greedling = monsterDieGreedling("Greedling", "test image.jpg", 2, 1, 5, 0, [CoinStack(7)])
    additionalEnemyDeck.addCardTop(greedling)
    hanger = monsterDieExpandShop("Hanger", "test image.jpg", 2, 2, 4, 0, [CoinStack(7)], 1)
    additionalEnemyDeck.addCardTop(hanger)
    hopper = monsterRollImmunity("Hopper", "test image.jpg", 2, 1, 3, 0, [CoinStack(3)], 6)
    additionalEnemyDeck.addCardTop(hopper)
    horf = monsterRollHorf("Horf", "test image.jpg", 1, 1, 4, 0, [CoinStack(3)])
    additionalEnemyDeck.addCardTop(horf)
    leaper = monsterRollLeaper("Leaper", "test image.jpg", 2, 1, 4, 0, [CoinStack(5)])
    additionalEnemyDeck.addCardTop(leaper)
    keeper_head = monsterDamageKeeperHead("Keeper Head", "test image.jpg", 2, 1, 4, 0, [CoinXReward()])
    additionalEnemyDeck.addCardTop(keeper_head)
    moms_dead_hand = monsterDieMomsDeadHand("Mom's Dead Hand", "test image.jpg", 2, 1, 5, 0, [CoinStack(4)])
    additionalEnemyDeck.addCardTop(moms_dead_hand)
    mulliboom = monsterDieMulliboom("Mulliboom", "test image.jpg", 1, 4, 2, 0, [CoinStack(6)])
    additionalEnemyDeck.addCardTop(mulliboom)
    mulligan = monsterDieMulligan("Mulligan", "test image.jpg", 1, 1, 3, 0, [CoinStack(3)])
    additionalEnemyDeck.addCardTop(mulligan)
    portal = monsterDieExtraMandatoryAttack("Portal", "test image.jpg", 2, 1, 4, 0, [CoinStack(3)])
    additionalEnemyDeck.addCardTop(portal)
    conquest = monsterDieExtraAttack("Conquest", "test image.jpg", 2, 1, 3, 1, [CoinStack(6)])
    additionalEnemyDeck.addCardTop(conquest)
    envy = monsterDieExtraAttack("Envy", "test image.jpg", 2, 1, 5, 1, [CoinStack(1)])
    additionalEnemyDeck.addCardTop(envy)
    psy_horf = monsterDiePsyHorf("Psy Horf", "test image.jpg", 1, 1, 5, 0, [LootReward(1)])
    additionalEnemyDeck.addCardTop(psy_horf)
    rage_creep = monsterDamageRageCreep("Rage Creep", "test image.jpg", 1, 1, 5, 0, [LootReward(2)])
    additionalEnemyDeck.addCardTop(rage_creep)
    ring_of_flies = monsterRollRingOfFlies("Ring of Flies", "test image.jpg", 3, 1, 3, 0, [CoinStack(3)])
    additionalEnemyDeck.addCardTop(ring_of_flies)
    swarm_of_flies = monsterRollSwarmOfFlies("Swarm of Flies", "test image.jpg", 5, 1, 2, 0, [CoinStack(5)])
    additionalEnemyDeck.addCardTop(swarm_of_flies)
    wizoob = monsterDieDestroySoul("Wizoob", "test image.jpg", 3, 1, 5, 0, [LootReward(3)])
    additionalEnemyDeck.addCardTop(wizoob)
    carrion_queen = monsterRollCarrionQueen("Carrion Queen", "test image.jpg", 4, 1, 3, 1, [CoinStack(7)])
    additionalEnemyDeck.addCardTop(carrion_queen)
    pin = monsterRollImmunity("Pin", "test image.jpg", 2, 1, 4, 1, [CoinStack(7)], 6)
    additionalEnemyDeck.addCardTop(pin)
    the_lamb = monsterDieStealSoul("The Lamb", "test image.jpg", 6, 6, 3, 1, [CoinStack(3)])
    additionalEnemyDeck.addCardTop(the_lamb)
    death = monsterDieKillPlayer("Death", "test image.jpg", 3, 2, 4, 1, [TreasureReward(1)])
    additionalEnemyDeck.addCardTop(death)
    gemini = monsterHpGemini("Gemini", "test image.jpg", 3, 1, 4, 1, [CoinStack(5)])
    additionalEnemyDeck.addCardTop(gemini)
    gluttony = monsterRollGluttony("Gluttony", "test image.jpg", 4, 1, 3, 1, [LootReward(1)])
    additionalEnemyDeck.addCardTop(gluttony)
    greed = monsterDamageGreed("Greed", "test image.jpg", 3, 1, 4, 1, [CoinStack(9)])
    additionalEnemyDeck.addCardTop(greed)
    dark_one = monsterHurtDamageUp("Dark One", "test image.jpg", 3, 1, 4, 1, [TreasureReward(1)])
    additionalEnemyDeck.addCardTop(dark_one)
    larry_jr = monsterHpLarryJr("Larry Jr.", "test image.jpg", 4, 1, 3, 1, [CoinStack(1)])
    additionalEnemyDeck.addCardTop(larry_jr)
    lust = monsterHurtLust("Lust", "test image.jpg", 2, 1, 4, 1, [LootReward(2)])
    additionalEnemyDeck.addCardTop(lust)
    mask_of_infamy = monsterHpMaskOfInfamy("Mask of Infamy", "test image.jpg", 4, 1, 4, 1, [TreasureReward(1)])
    additionalEnemyDeck.addCardTop(mask_of_infamy)
    mega_fatty = monsterDamageMegaFatty("Mega Fatty", "test image.jpg", 3, 1, 3, 1, [LootReward(2)])
    additionalEnemyDeck.addCardTop(mega_fatty)
    scolex = monsterDamageScolex("Scolex", "test image.jpg", 3, 1, 5, 1, [TreasureReward(1)])
    additionalEnemyDeck.addCardTop(scolex)
    sloth = monsterDieSloth("Sloth", "test image.jpg", 3, 1, 4, 1, [CoinStack(1)])
    additionalEnemyDeck.addCardTop(sloth)
    war = monsterHurtDamageUp("War", "test image.jpg", 3, 1, 3, 1, [CoinStack(8)])
    additionalEnemyDeck.addCardTop(war)
    the_bloat = monsterDamageTheBloat("The Bloat", "test image.jpg", 4, 2, 4, 1, [TreasureReward(1)])
    additionalEnemyDeck.addCardTop(the_bloat)
    the_duke_of_flies = monsterHurtTheDukeOfFlies("The Duke of Flies", "test image.jpg", 4, 1, 3, 1, [LootReward(2)])
    additionalEnemyDeck.addCardTop(the_duke_of_flies)
    pestilence = monsterDiePestilence("Pestilence", "test image.jpg", 4, 1, 4, 1, [LootReward(2)])
    additionalEnemyDeck.addCardTop(pestilence)
    wrath = monsterDieWrath("Wrath", "test image.jpg", 3, 1, 3, 1, [CoinStack(6)])
    additionalEnemyDeck.addCardTop(wrath)
    mom = monsterRollDieMom("Mom!", "test image.jpg", 5, 2, 4, 2, [TreasureReward(1)])
    additionalEnemyDeck.addCardTop(mom)
    satan = monsterRollSatan("Satan!", "test image.jpg", 6, 2, 4, 2, [TreasureReward(2)])
    additionalEnemyDeck.addCardTop(satan)
    return additionalEnemyDeck

def createAllEnemies():
    basicE = createBasicEnemyCards()
    basicB = createBasicBossCards()
    # add all the decks together
    allEnemies = Deck([])
    allEnemies.combineDeck(basicE)
    allEnemies.combineDeck(basicB)
    return allEnemies



