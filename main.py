import analyze
import constants
from parse import read_data
import os
import sys


def main():
    print(sys.argv)
    if len(sys.argv) < 3:
        print('Expected "show/save" then type of analysis')
        return

    fig_option = sys.argv[1]

    if fig_option not in ["show", "save"]:
        print('Expected "show/save" as first option')
        return

    analyze_option = sys.argv[2]
    data = read_data()
    fig = analyze.get_fig(analyze_option, data)

    if fig_option == "show":
        fig.show()
    elif fig_option == "save":
        if len(sys.argv) > 3:
            print("Expected filename to save")
            return
        name = sys.argv[2]
        filepath = os.path.join(constants.IMAGE_FOLDER, name)
        fig.write_image(filepath)


main()
