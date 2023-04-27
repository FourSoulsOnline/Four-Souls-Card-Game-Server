# Contributors: Jackson Cashman
class CoinStack:
    def __init__(self, count):
        self.count = count

    def getCount(self):
        return self.count
    
    def getJsonObject(self):
        coinStackObject = {
            "name": "CoinStack",
            "count": self.count
        }
        return coinStackObject

    # adds the coins from CoinStack c2 into self.count
    def combine(self, c2):
        self.count += c2.count
        return

# logic for coinX is in die effect
class CoinXReward:
    def __init__(self):
        return
    
    def getJsonObject(self):
        coinXRewardObject = {
            "name": "CoinXReward"
        }
        return coinXRewardObject

'''
# example of creating coins and adding them

myCoin = CoinStack(5)
print(myCoin.getCount())
myCoin2 = CoinStack(2)
myCoin.combine(myCoin2)
print(myCoin.getCount())
'''