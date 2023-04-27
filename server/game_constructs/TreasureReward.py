# Contributors: Jackson Cashman
'''
Rewards from Enemies & etc to "Gain X Treasure"
'''

# count is the amount of Treasure the Player will gain
class TreasureReward:
    def __init__(self, count):
        self.count = count

    def getCount(self):
        return self.count
    
    def getJsonObject(self):
        treasureRewardObject = {
            "name": "TreasureRewardObject",
            "count": self.count
        }
        return treasureRewardObject