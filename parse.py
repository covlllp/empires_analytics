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
        },
        points: {
            player: Number[]
        },
        moves: [
            {
                type: String (start, end, move)
                empire: String?
                player: String?
                territory: String?
                action: String (attack, defeat, tie, expand, start)
            },...
        ]
    }, ...
]
"""


def sanitize_entry(entry):
    return entry.replace(
        ".", ""
    ).replace("The ", "")


def read_data():
    results = []

    for filename in os.listdir(constants.DATA_FOLDER):
        result = dict(name=os.path.splitext(filename)[0])
        empires = {name: [] for name in constants.PLAYERS}
        points = {name: [] for name in constants.PLAYERS}
        moves = []

        def add_move(empire, territory, action):
            empire = sanitize_entry(empire)
            territory = sanitize_entry(territory)
            moves.append(dict(type="move", empire=empire,
                         territory=territory, action=action))

        filepath = os.path.join(constants.DATA_FOLDER, filename)
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
                empire = " ".join(words[play_index + 1: empire_end_index])
                empire = sanitize_entry(empire)
                empires[player].append(empire)
                moves.append(dict(type="start", player=player, empire=empire))
            elif "scored" in line:
                player = words[1]
                point = int(words[3])
                points[player].append(point)
                moves.append(dict(type="end", player=player))
            elif "The game is over" in line:
                winner = words[4][5:]
                result["winner"] = winner
            elif "expand" in line:
                expand_index = words.index("expand")
                into_index = words.index("into")
                empire = " ".join(words[1: expand_index])
                territory = " ".join(words[into_index + 1: len(words)])
                add_move(empire, territory, "expand")
            elif "has appeared" in line or "have appeared" in line:
                appeared_index = words.index("appeared")
                in_index = words.index("in")
                empire = " ".join(words[1:appeared_index - 1])
                territory = " ".join(words[in_index + 1: len(words)])
                add_move(empire, territory, "start")
            elif "were defeated" in line:
                defeated_index = words.index("defeated")
                by_index = words.index('by')
                empire = " ".join(words[1:defeated_index - 1])
                territory = " ".join(words[defeated_index + 2: by_index])
                add_move(empire, territory, "defeat")
            elif "defeated" in line and "occupied" in line:
                defeated_index = words.index("defeated")
                occupied_index = words.index('occupied')
                empire = " ".join(words[1:defeated_index])
                territory = " ".join(words[occupied_index + 1: len(words)])
                add_move(empire, territory, "attack")
            elif "destroyed each other" in line:
                and_index = words.index("and")
                in_index = words.index("in")
                empire = " ".join(words[1:and_index])
                territory = " ".join(words[in_index + 1: len(words)])
                add_move(empire, territory, "tie")

        result["empires"] = empires
        result["points"] = points
        result["moves"] = moves
        results.append(result)

    return results
