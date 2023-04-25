

class ReduceDamage:
    def __init__(self, dmgAmount):
        self.shield = dmgAmount
        self.tag = ["reduce damage"]

    def getShield(self):
        return self.shield

    def getTag(self):
        return self.tag

    def effect(self, dmg):
        if self.shield >= dmg:
            return 0
        else:
            return dmg - self.shield


# dice roll effects

# declare attack effect

# take damage effect

# gaining money

# start of turn effect

# first attack effect

# end of turn effect

# if player have certain loot cards in hand or money

# character die effect

# play additional loot

# activating an item

# if item is destroyed