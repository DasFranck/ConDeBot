#!/usr/bin/env python3
# -*- coding: utf-8 -*-

NAME = "ConDeBot"
QUOTES = ["Without sugar.", "With one sugar.", "With too much sugar.",
          "With a pinch of sugar.", "With three spoon of salt because I hate you so much.",
          "With a bit of milk", "Wait did I put a sugar? I'm not sure...", ""]

try:
    import random
except ImportError as message:
    print("Missing package(s) for %s: %s" % (NAME, message))
    exit(12)


def quote(author, args):
    # Check if the coffee is for someone else (And if the sender didn't forget the recipient)
    if ('>' in args):
        index = args.index('>') + 1
        return ("Here " + " ".join(args[index:]) + ", that's your coffee.\n" + random.choice(QUOTES))
    else:
        return ("Here " + author + ", that's your coffee.\n" + random.choice(QUOTES))
