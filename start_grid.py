#!/usr/bin/env python3

import argparse
import json
import os
import subprocess

DRIVERS = "~/.wdm"
GRID = "~/Downloads/selenium-server-4.2.1.jar"
YANDEX = DRIVERS + '/drivers/yandexdriver/linux64/latest'

parser = argparse.ArgumentParser()

parser.add_argument('--mode', default='standalone',
                    choices=('standalone', 'hub', 'node'))
parser.add_argument('--host', default='127.0.0.1')
parser.add_argument('--port')
parser.add_argument('--jar', default=os.path.expanduser(GRID))
parser.add_argument('--wdm', default=os.path.expanduser(DRIVERS))

args = parser.parse_args()


def main():
    try:
        with open(os.path.expanduser(args.wdm).rstrip('/') + '/drivers.json', 'r') as f:
            d = json.load(f)
    except Exception:
        print('Could not open WDM config')
        exit()

    my_env = os.environ.copy()
    my_env['PATH'] = f"{os.getenv('PATH')}:" + ':'.join(
        [f"{v['binary_path'].rsplit('/', 1)[0]}" for v in d.values()]) + f':{os.path.expanduser(YANDEX)}'

    my_command = ["java", "-jar", args.jar, args.mode, "--host", args.host, "--log-level", "ALL"]
    if args.port:
        my_command.extend(["--port", args.port])

    subprocess.run(my_command, env=my_env)


if __name__ == '__main__':
    main()
