import configparser
import glob
import os

import time

import stats
from reviews import reviews

config = {}
file_tree = {}


def init():
    global config
    abs_dirpath = '/'.join(os.path.abspath(__file__).split('/')[:-1]) + '/'
    config_parser = configparser.ConfigParser()
    config_parser.read(abs_dirpath + 'config.ini')

    for (key, value) in config_parser.items(config_parser.default_section):
        config[key] = value

    if not os.path.exists(config['data_directory']):
        os.makedirs(config['data_directory'])


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


def get_general_stats():
    current_ts = int(time.time())
    for var in (v for v in dir(stats) if not v.startswith('_')):
        path = os.path.join(config['data_directory'], '{0}.csv'.format(var))
        with open(path, 'a') as file:
            # print(var, '=', eval('stats.' + var))
            line = '{0},{1}\n'.format(current_ts, eval('stats.' + var))
            file.write(line)


def print_tree():
    for file in sorted(file_tree.keys()):
        # if 'nova/tests/unit/objects/test_instance.py' in file:
        file = get_file_repo_path(file)
        print(get_file_repo_path(file))
        # reviews(file)


def get_file_repo_path(path):
    path = path.split('/')
    index = path.index('nova')
    return '/'.join(path[index+1:])

if __name__ == '__main__':
    init()
    build_file_tree()
    get_general_stats()
    print_tree()
