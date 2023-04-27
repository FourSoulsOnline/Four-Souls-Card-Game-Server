import sys
import time
import json

discardLoot = {
    "messageFlag": "DISCARD-LOOT",
    "cards": ["Eden", "Eden", "Eden", "Eden", "Eden", "Eden", "Eden", "Eden", "Eden", "Eden", "Eden", "Eden"]
}
print(json.dumps(discardLoot))
sys.stdout.flush()
time.sleep(1)

discardMonster = {
    "messageFlag": "DISCARD-MONSTER",
    "cards": ["Big Spider", "Big Spider", "Big Spider", "Big Spider", "Big Spider", "Big Spider", "Big Spider", "Big Spider","Big Spider", "Big Spider","Big Spider", "Big Spider","Big Spider", "Big Spider"]
}
print(json.dumps(discardMonster))
sys.stdout.flush()
time.sleep(1)

discardTreasure = {
    "messageFlag": "DISCARD-TREASURE",
    "cards": ["Box!", "Box!", "Box!", "Box!", "Box!", "Box!", "Box!", "Box!", "Box!", "Box!", "Box!", "Box!", "Box!", "Box!"]
}
print(json.dumps(discardTreasure))
sys.stdout.flush()
time.sleep(1)