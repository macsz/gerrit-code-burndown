import configparser
import glob
import os

import time

import datetime

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
        zip_data(path)


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


def zip_data(path):
    class Data(object):
        time_start = 9999999999
        time_end = 0
        value = 0
        num = 0

        def change_dates(self, date):
            if date < self.time_start:
                self.time_start = date
            if date > self.time_end:
                self.time_end = date

        def __str__(self):
            return '{0}: {1}-{2}'.format(
                self.value,
                datetime.datetime.fromtimestamp(self.time_start).strftime(
                    '%Y-%m-%d %H:%M:%S'),
                datetime.datetime.fromtimestamp(self.time_end).strftime(
                    '%Y-%m-%d %H:%M:%S'),)

    timeline = {}
    with open(path, 'r') as f:
        for line in f:
            line = line.split(',')
            t = int(line[0])
            v = int(line[1])

            if v not in timeline.keys():
                timeline[v] = Data()
                timeline[v].value = v
            timeline[v].change_dates(t)
    zip_file = path.split('.')
    zip_file[-2] = zip_file[-2] + '_zip'
    zip_file = '.'.join(zip_file)
    with open(zip_file, 'w') as f:
        for t in timeline:
            f.write('{0},{1}\n'.format(timeline[t].time_start,
                                       timeline[t].value))
            f.write('{0},{1}\n'.format(timeline[t].time_end,
                                       timeline[t].value))

if __name__ == '__main__':
    init()
    build_file_tree()
    get_general_stats()
    print_tree()
    zip_data('data/num_matched_files.csv')
