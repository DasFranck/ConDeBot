#!/usr/bin/env python3
# -*- coding: utf-8 -*-

NAME = "ConDeBot"

try:
    import random
    import json
except ImportError as message:
    print("Missing package(s) for %s: %s" % (NAME, message))
    exit(12)


def coffee(client, logger, message, action, args, author):
    # Check if the coffee is for someone else (And if the sender didn't forget the recipient)
    with open("jsonfiles/coffee.json", 'r') as quotes_file:
        quotes = json.load(quotes_file)
        if ('>' in args):
            index = args.index('>') + 1
            return ("Here " + " ".join(args[index:]) + ", that's your coffee.\n" + random.choice(quotes["coffee"]))
        else:
            return ("Here " + message.author.mention + ", that's your coffee.\n" + random.choice(quotes["coffee"]))


def tea(client, logger, message, action, args, author):
    # Check if the coffee is for someone else (And if the sender didn't forget the recipient)
    with open("jsonfiles/coffee.json", 'r') as quotes_file:
        quotes = json.load(quotes_file)
        if ('>' in args):
            index = args.index('>') + 1
            return ("Here " + " ".join(args[index:]) + ", that's your tea.\n" + random.choice(quotes["tea"]))
        else:
            return ("Here " + message.author.mention + ", that's your tea.\n" + random.choice(quotes["tea"]))
