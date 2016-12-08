#!/usr/bin/env python3
# -*- coding: utf-8 -*-

NAME = "ConDeBot"

try:
    import random
    import json
except ImportError as message:
    print("Missing package(s) for %s: %s" % (NAME, message))
    exit(12)


def coffee(author, args):
    # Check if the coffee is for someone else (And if the sender didn't forget the recipient)
    with open("jsonfiles/coffee.json", 'r') as quotes_file:
        quotes = json.load(quotes_file)
        if ('>' in args):
            index = args.index('>') + 1
            return ("Here " + " ".join(args[index:]) + ", that's your coffee.\n" + random.choice(quotes["coffee"]))
        else:
            return ("Here " + author + ", that's your coffee.\n" + random.choice(quotes["coffee"]))


def tea(author, args):
    # Check if the coffee is for someone else (And if the sender didn't forget the recipient)
    with open("jsonfiles/coffee.json", 'r') as quotes_file:
        quotes = json.load(quotes_file)
        if ('>' in args):
            index = args.index('>') + 1
            return ("Here " + " ".join(args[index:]) + ", that's your tea.\n" + random.choice(quotes["tea"]))
        else:
            return ("Here " + author + ", that's your tea.\n" + random.choice(quotes["tea"]))
