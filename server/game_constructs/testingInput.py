# messageFlag: CHOICE
import sys
import json
import time
import zlib
import gzip

# Sample data to be compressed
outputMessage = "OMG THIS FUCKING WORKS"
systemMessage = {"messageFlag": "SYSTEM", "systemMessage": outputMessage}

json_data = json.dumps(systemMessage)

# Compress the data using gzip
compressed_data = gzip.compress(json_data.encode())

# Write the compressed data to stdout
sys.stdout.buffer.write(compressed_data)


# while True:
#     choiceMessage = {
#         "messageFlag": "CHOICE",
#         "socketID": "player.getSocketId()",
#         "choiceMessage": "It's your turn! What would you like to do?",
#         "choices": ["Play a Loot Card", "Activate an Item", "Attack a Monster!"]
#     }

#     print(json.dumps(choiceMessage))
#     sys.stdout.flush()
#     inp = int(input())
#     time.sleep(1)
#     # Handle logic after input
#     outputMessage = "You chose: " + choiceMessage['choices'][inp]
#     systemMessage = {
#         "messageFlag": "SYSTEM",
#         "systemMessage": outputMessage
#     }
#     print(json.dumps(systemMessage))
#     sys.stdout.flush()
#     time.sleep(1)
