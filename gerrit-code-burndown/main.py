import configparser
import glob
import os

import stats

config = {}
file_tree = {}


def init():
    global config
    abs_dirpath = '/'.join(os.path.abspath(__file__).split('/')[:-1]) + '/'
    config_parser = configparser.ConfigParser()
    config_parser.read(abs_dirpath + 'config.ini')

    for (key, value) in config_parser.items(config_parser.default_section):
        config[key] = value


def build_file_tree():
    global file_tree
    all_files = sorted(glob.iglob('%s/**/*.py' % config['search_directory'],
                                  recursive=True))
    stats.num_all_files = len(all_files)

    for test_file in all_files:
        with open(test_file) as f:
            local_file_tree = []
            line_number = 0
            for line in f:
                line_number += 1
                if config['keyword'] in line:
                    stats.num_matched_lines += 1
                    line = line.strip()
                    local_file_tree.append((line_number, line))
            if local_file_tree:
                file_tree[test_file] = local_file_tree
    stats.num_matched_files = len(file_tree)


def print_stats():
    for var in (v for v in dir(stats) if not v.startswith('_')):
        print(var, '=', eval('stats.'+var))

if __name__ == '__main__':
    init()
    build_file_tree()
    print_stats()

# import glob
#
# TARGET_PHRASE = 'mox'
# TOP = 'nova/nova/tests'
# NUM_ALL_FILES = 0
# NUM_MATCHED_FILES = 0
# FILE_TREE = {}
#
#
# def get_all_test_files():
#     global NUM_ALL_FILES
#     all_files = sorted(glob.iglob('%s/**/*.py' % TOP, recursive=True))
#     NUM_ALL_FILES = len(all_files)
#     return all_files
#
#
# def construct_tree():
#     global FILE_TREE
#     global NUM_MATCHED_FILES
#     FILE_TREE = {}
#     for test_file in get_all_test_files():
#         with open(test_file) as f:
#             local_mox_tree = []
#             line_number = 0
#             for line in f:
#                 line_number += 1
#                 if TARGET_PHRASE in line:
#                     line = line.strip()
#                     local_mox_tree.append((line_number, line))
#             if local_mox_tree:
#                 FILE_TREE[test_file] = local_mox_tree
#     NUM_MATCHED_FILES = len(FILE_TREE)
#
# if __name__ == '__main__':
#     construct_tree()
#     for key in FILE_TREE.keys():
#         print(key)
#         for val in FILE_TREE[key]:
#             print('\t', val)
#     print(NUM_MATCHED_FILES/NUM_ALL_FILES)