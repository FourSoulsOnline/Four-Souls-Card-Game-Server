# Contributors: Jackson Cashman
'''
Rewards from Enemies & etc to "Loot X cards"
'''
from Dice import Dice

# count is the amount of Loot the Player will draw
class LootReward:
    def __init__(self, count):
        self.count = count

    def getCount(self):
        return self.count
    
    def getJsonObject(self):
        lootRewardObject = {
            "name": "LootReward",
            "count": self.count
        }
        return lootRewardObject

# logic for coinX is in die effect
class LootXReward:
    def __init__(self):
        return
    
    def getJsonObject(self):
        lootXRewardObject = {
            "name": "LootXReward"
        }
        return lootXRewardObject
