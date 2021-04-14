"""
Functions here take data shapes defined in parse.py
and return px fig
"""

from collections import defaultdict
import pandas
import plotly.express as px


def get_fig(option, data):
    if option == "empire_wins":
        return get_winning_empires(data)
    elif option == "starting_empire_wins":
        return get_winning_empires(data, epoch=0)
    elif option == "epoch_points_max":
        return get_epoch_points(data, direction="max")
    elif option == "epoch_points_min":
        return get_epoch_points(data, direction="min")
    else:
        print("Option incorrect")
        return


def get_winning_empires(data, epoch=None):
    winning_empires_dict = defaultdict(lambda: 0)

    for game in data:
        winner = game["winner"]
        if epoch is None:
            empires = game["empires"][winner]
        else:
            empires = [game["empires"][winner][epoch]]
        for empire in empires:
            winning_empires_dict[empire] = winning_empires_dict[empire] + 1

    empires = []
    win_count = []
    for key in winning_empires_dict:
        empires.append(key)
        win_count.append(winning_empires_dict[key])

    df = pandas.DataFrame({"Empire": empires, "Wins": win_count}).sort_values("Wins")
    fig = px.bar(df, x="Empire", y="Wins")
    return fig


def get_epoch_points(data, direction="max"):
    max_epoch_dict = defaultdict(lambda: -1000)
    min_epoch_dict = defaultdict(lambda: 1000)

    for game in data:
        for player in game["points"]:
            epoch = 0
            for point in game["points"][player]:
                max_epoch_dict[epoch] = max(max_epoch_dict[epoch], point)
                min_epoch_dict[epoch] = min(min_epoch_dict[epoch], point)
                epoch = epoch + 1

    epochs = []
    points = []
    for epoch in max_epoch_dict:
        epochs.append(epoch)
        epoch_dict = min_epoch_dict if direction == "min" else max_epoch_dict
        points.append(epoch_dict[epoch])
    df = pandas.DataFrame({"Epoch": epochs, "Points": points}).sort_values("Epoch")
    return px.bar(df, x="Epoch", y="Points")
