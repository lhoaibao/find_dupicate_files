#!/usr/bin/env python3
import argparse
import os
from itertools import groupby


# --------------Waypoint 1---------------------
def initialize_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', required=True, help="root path", action='store')
    return parser.parse_args()


#---------------Waypoint 2---------------------
def scan_files(path):
    list_file = []
    for root, dirs, files in os.walk(path):
        for name in files:
            list_file.append(os.path.join(root, name))
    return list_file


#---------------Waypoint 3----------------------
def group_files_by_size(file_path_names):
    pass


def main():
    args = initialize_argparse()
    file_path_names = can_files(args.path)


if __name__ == '__main__':
    main()
