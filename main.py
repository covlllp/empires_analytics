from collections import defaultdict
import pandas
from parse import read_data
import plotly.express as px

data = read_data()

winning_empires_dict = defaultdict(lambda: 0)

for game in data:
    winner = game["winner"]
    for empire in game["empires"][winner]:
        winning_empires_dict[empire] = winning_empires_dict[empire] + 1

empires = []
win_count = []
for key in winning_empires_dict:
    empires.append(key)
    win_count.append(winning_empires_dict[key])

df = pandas.DataFrame({"Empire": empires, "Wins": win_count}).sort_values("Wins")

fig = px.bar(df, x="Empire", y="Wins")
fig.write_image("images/test.jpg")
fig.show()
