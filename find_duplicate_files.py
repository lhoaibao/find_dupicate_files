#!/usr/bin/env python3
"""
-project name: find_duplicate_files
-creater: lhoaibao
-version: v1
-purpose: find all the file has the same content recursively in the root path
          and return it.
"""

# ---------------Library import ----------------
from time import time
from json import dumps
import argparse
from os import access, F_OK, R_OK, walk, stat
from os.path import isdir, islink, join
from hashlib import md5


# --------------Waypoint 1---------------------
def initialize_argparse():
    """
    initialize argparse module for control the command
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path',
                        required=True, help="root path", action='store')
    parser.add_argument('-n', '--nice',
                        help='print pretty type', action='store_true')
    parser.add_argument('-b', '--bonus', action='store_true')
    return parser.parse_args()


def valid_path(path):
    """
    function check the root path is valid or not
    """
    return (isdir(path) and access(path, F_OK) and access(path, R_OK))


def valid_file(file_path_name):
    """
    function check the file_path_name is valid or not
    """
    return (access(file_path_name, F_OK) and
            access(file_path_name, R_OK) and not
            islink(file_path_name))


# ---------------Waypoint 2---------------------
def scan_files(path):
    """
    find all the file from the root path recursively and return it by a list'
    input: root path
    output: list of file
    """
    list_file = []
    for root, dirs, files in walk(path):
        for name in files:
            file_path_name = join(root, name)
            if valid_file(file_path_name):
                list_file.append(join(root, name))
    if not list_file:
        return None
    return list_file


# -------------help function--------------------
def check_duplicate(dict):
    """
    help to get the groups file has the same adj like size or content has more
    than 2 files
    input: a dict
    output: a list of list store groups of file has same adj and has more than
            2 item
    """
    groups = []
    for item in dict:
        if len(dict[item]) >= 2:
            groups.append(dict[item])
    return groups


# ---------------Waypoint 3----------------------
def group_files_by_size(file_path_names):
    """
    get the list of file and divide it into each groups has same size
    input: list of file
    output: list of same size files
    """
    dict = {}
    for index, item in enumerate(file_path_names):
        file_size = stat(item).st_size
        if file_size == 0:
            continue
        if file_size not in dict:
            dict[file_size] = [item]
        else:
            dict[file_size].append(item)
    return check_duplicate(dict)


# ---------------Waypoint 4-----------------------
def get_file_checksum(file_path_name):
    """
    get the md5 of content file
    input: file path name
    output: md5
    """
    with open(file_path_name, 'rb') as f:
        f_content = f.read()
    return md5(f_content).hexdigest()


# ---------------Waypoint 5-----------------------
def group_files_by_checksum(file_path_names):
    """
    get the list of file and divide it into each groups has same content
    input: list of file
    output: list of same content files
    """
    dict = {}
    for item in file_path_names:
        md5 = get_file_checksum(item)
        if md5 not in dict:
            dict[md5] = [item]
        else:
            dict[md5].append(item)
    return check_duplicate(dict)


# ---------------Waypoint 6-----------------------
def find_duplicate_files(file_path_names):
    """
    find all duplicate file by the root path
    and return it by type list
    input: file_path_name
    output: list of file duplicate
    """
    duplicate_files = []
    group_file = group_files_by_size(file_path_names)
    for item in group_file:
        if item:
            duplicate_files.extend(group_files_by_checksum(item))
    return duplicate_files


# -------------bonus------------------------------
def do_compare(file1, file2):
    """ To compare two file if equal or not
    Input: two file
    Output: true if they are equal and false if not
    """
    bufsize = 1024
    with open(file1, 'rb') as fp1, open(file2, 'rb') as fp2:
        while True:
            kb_f1 = fp1.read(bufsize)
            kb_f2 = fp2.read(bufsize)
            if kb_f1 != kb_f2:
                return False
            if not kb_f1:
                return True


def group_files_by_compare(file_path_names):
    """ To group files by function do_cmp
    Input: file_path_names, corresponding to a flat list of the
    absolute path and name of files
    Output: a list of groups of duplicate files.
    """
    try:
        res = []
        while len(file_path_names) > 0:
            first = file_path_names.pop(0)
            tmp = [first]
            for i in file_path_names:
                if do_compare(first, i):
                    tmp.append(i)
            file_path_names = list(set(file_path_names) - set(tmp))
            res.append(tmp)
        return res
    except Exception:
        exit("Error in group files by comparing")


def find_duplicate_files_bonus(file_path_names):
    """ To find all duplicate files use the two previous functions
    group_files_by_size and group_files_by_compare
    Input: file_path_names, corresponding to a list of absolute path
    and name of files
    Output: a list of groups of duplicate files.
    """
    res = []
    tmpres = group_files_by_size(file_path_names)
    for i in tmpres:
        res = res + group_files_by_compare(i)
    return res


def main():
    start = time()
    args = initialize_argparse()
    if not valid_path(args.path):
        print('path is wrong')
        return
    file_path_names = scan_files(args.path)
    if not file_path_names:
        print('path is wrong')
        return
    if args.bonus:
        duplicate_files = find_duplicate_files_bonus(file_path_names)
    else:
        duplicate_files = find_duplicate_files(file_path_names)
    if args.nice:
        print(dumps(duplicate_files, indent=True))
    else:
        print(dumps(duplicate_files))
    end = time()
    print('time: ', str(end-start))


if __name__ == '__main__':
    main()
