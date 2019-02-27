#!/usr/bin/env python3

#---------------Library import ----------------
import argparse
import os
import hashlib
import json


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


#-------------help function--------------------
def check_duplicate(dict):
    groups = []
    for item in dict:
        if len(dict[item]) >= 2:
            groups.append(dict[item])
    return groups


#---------------Waypoint 3----------------------
def group_files_by_size(file_path_names):
    dict = {}
    for index, item in enumerate(file_path_names):
        file_size = os.stat(item).st_size
        if file_size not in dict:
            dict[file_size] = [item]
        else:
            dict[file_size].append(item)
    return check_duplicate(dict)


#---------------Waypoint 4-----------------------
def get_file_checksum(file_path_name):
    with open(file_path_name) as f:
        f_content = f.read()
        f_content = f_content.encode()
    return hashlib.md5(f_content).hexdigest()


#---------------Waypoint 5-----------------------
def group_files_by_checksum(file_path_names):
    dict = {}
    for item in file_path_names:
        md5 = get_file_checksum(item)
        if md5 not in dict:
            dict[md5] = [item]
        else:
            dict[md5].append(item)
    return check_duplicate(dict)


#---------------Waypoint 6-----------------------
def find_duplicate_files(file_path_names):
    duplicate_files = []
    group_file = group_files_by_size(file_path_names)
    for item in group_file:
        if item:
            duplicate_files.extend(group_files_by_checksum(item))
    return duplicate_files


def main():
    args = initialize_argparse()
    file_path_names = scan_files(args.path)
    duplicate_files = find_duplicate_files(file_path_names)
    print(json.dumps(duplicate_files))


if __name__ == '__main__':
    main()
