import os

import constants

"""
Response structure:
[
    {
        name: String(game_name),
        winner: String(winner),
        empires: {
            player: String(empire)[]
        }
    }, ...
]
"""


def read_data():
    results = []

    for filename in os.listdir(constants.DATA_FOLDER):
        result = dict(name=os.path.splitext(filename)[0])
        empires = {name: [] for name in constants.PLAYERS}

        filepath = os.path.join(constants.DATA_FOLDER, filename)
        print("Reading '%s'" % filepath)

        file = open(filepath)

        lines = file.readlines()
        for line in lines:
            words = line.split()
            if "plays" in line:
                player = words[1]
                play_index = words.index("plays")
                empire_end_index = (
                    words.index("with") if "with" in words else len(words)
                )
                empire = " ".join(words[play_index + 1 : empire_end_index]).replace(
                    ".", ""
                )

                empires[player].append(empire)

            elif "The game is over" in line:
                winner = words[4][5:]
                result["winner"] = winner

        result["empires"] = empires
        results.append(result)

    return results
