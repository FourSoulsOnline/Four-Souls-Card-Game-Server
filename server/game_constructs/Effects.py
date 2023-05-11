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
