#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def get_nickdis(user):
    return (user.name + "#" + str(user.discriminator))


def get_meta(cdb, message):
    msg = message.content
    args = msg.split(" ")
    if (message.author == cdb.user or msg is None or len(args[0]) == 0):
        return (None, None, None, None, None)
    author = get_nickdis(message.author)

    if (cdb.PREF == ""):
        triggered = args[0][0] == "!"
        action = args[0][1:] if len(args[0]) > 0 else ""
        args = args[1:]
    else:
        triggered = args[0] == ("!" + cdb.PREF)
        action = msg.split(" ")[1] if len(msg.split(" ")) > 1 else ""
        args = args[2:]

    return (msg, args, author, triggered, action)
