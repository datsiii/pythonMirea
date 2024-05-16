import os
import stat


def show_items_in_(path):
    for entry in os.listdir(path):
        print(f'{entry}', end="	")


show_items_in_(".")


def show_stats_of_items_in(path):
    for entry in os.listdir(path):
        statinfo = os.stat(entry)
        print(f'{stat.filemode(statinfo.st_mode)} ', end="")
        print(f'{entry}')
