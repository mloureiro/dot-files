#!/usr/bin/env python

from argparse import ArgumentParser
from glob import glob
from os import path, rename, symlink


def get_file_list(directory):
    return map(path.basename, glob(directory))


def link_file(source, target, item):
    dot_file = make_dot_name(item)
    backup_file(target, dot_file)
    symlink(
        path.join(source, item),
        path.join(target, dot_file),
    )
    print('File linked: [' + item + ']')


def backup_file(directory, item):
    file_path = path.join(directory, item)
    if not path.exists(file_path):
        return

    backup_name = generate_backup_name(directory, item)
    rename(file_path, path.join(directory, backup_name))
    print('Backup file: [' + backup_name + ']')


def generate_backup_name(directory, item):
    attempts = 0
    while attempts < 10:
        file_name = item + '.backup' + ('' if attempts == 0 else str(attempts))
        if not path.exists(path.join(directory, file_name)):
            return file_name
        attempts += 1
    raise Exception('Could not find a backup file name for: ' + item)


def make_dot_name(item):
    return item if item[0] == '.' else '.' + item


if __name__ == '__main__':
    parser = ArgumentParser(description='Link dot files')
    parser.add_argument('source', help='Path to existing dot files directory')
    parser.add_argument('target', help='Path to where the links will be created')
    args = parser.parse_args()

    for item in get_file_list(args.source + '/*'):
        link_file(args.source, args.target, item)
