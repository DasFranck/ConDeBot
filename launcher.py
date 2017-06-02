#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import subprocess
import sys

from config import config

# Thanks Red-DiscordBot for this one
try:
    import pip
except ImportError:
    pip = None


# The Main.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token")
    parser.add_argument("--no-pip", action="store_true")
    parser.add_argument("--autorestart", action="store_true")
    args = parser.parse_args()

    if not args.no_pip:
        print("Downloading or updating requirements, please wait...")
        status_code = subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "--target", "lib", "-r", "requirements.txt"])
        if status_code == 0:
            print("\nRequirements setup completed.")
        else:
            print("\nRequirements setup failed.")

    if "token" in args:
        run_cdb(args.token, args.autorestart)
    elif "token" in config and len(config.token) != 0:
        run_cdb(config.token, args.autorestart)
    else:
        print("You should input a token via the config file or via arguments", file=sys.stderr)
    return


def run_cdb(token, autorestart):
    while True:
        try:
            code = subprocess.call((sys.executable, "ConDeBot.py", "--token", token))
        except KeyboardInterrupt:
            code = 0
            break
        else:
            if code == 0:
                break
            else:
                if not autorestart:
                    break

    print("ConDeBot has been terminated. Exit code: %d" % code)


if (__name__ == '__main__'):
    main()
