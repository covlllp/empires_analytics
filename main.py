import analyze
import constants
from parse import read_data
import os
import sys


def main():
    print(sys.argv)
    if len(sys.argv) < 3:
        print('Expected "show/save/html" then type of analysis')
        return

    fig_option = sys.argv[1]

    if fig_option not in ["show", "save", "html"]:
        print('Expected "show/save/html" as first option')
        return

    analyze_option = sys.argv[2]
    data = read_data()
    fig = analyze.get_fig(analyze_option, data)

    if fig_option == "show":
        fig.show()
    elif fig_option == "html":
        fig.write_html("index.html")
    elif fig_option == "save":
        if len(sys.argv) < 4:
            print("Expected filename to save")
            return
        name = sys.argv[3]
        filepath = os.path.join(constants.IMAGE_FOLDER, name)
        fig.write_image(filepath)


main()
