#!/usr/bin/env python

from os import devnull, path, environ
from subprocess import call
from argparse import ArgumentParser

DEV_NULL = open(devnull, 'w')


def require_module(module_name, check_callback, install_callback):
    try:
        print('Checking existence of module: [' + module_name + ']')
        if not check_callback():
            raise Exception
        print('Successfully found module: [' + module_name + ']')
    except Exception:
        print('Missing module: [' + module_name + ']')
        install_module(module_name, install_callback)


def install_module(module_name, install_callback):
    try:
        print('Starting installation of module: [' + module_name + ']')
        if not install_callback():
            raise Exception
        print('Successfully installed module: [' + module_name + ']')
    except Exception:
        print('Failed to install [' + module_name + ']')
        raise


def require_brew():
    require_module(
        'brew',
        lambda: call(['brew', '--version'], stdout=DEV_NULL, stderr=DEV_NULL) == 0,
        lambda: call(
            '/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"',
            shell=True
        ) == 0,
    )


def require_zsh():
    require_module(
        'zsh',
        lambda: call(['zsh', '-c', 'ls']) == 0,
        lambda: call(['brew', 'install', 'zsh']) == 0,
    )


def require_oh_my_zsh():
    require_module(
        'oh-my-zsh',
        lambda: call(['ls', environ['HOME'] + '/.oh-my-zsh'], stdout=DEV_NULL, stderr=DEV_NULL) == 0,
        lambda: call(
            'sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"',
            shell=True,
        ) == 0,
    )


if __name__ == '__main__':
    parser = ArgumentParser(description='Setup shell')
    args = parser.parse_args()

    require_brew()
    require_zsh()
    require_oh_my_zsh()
    print('Done')
