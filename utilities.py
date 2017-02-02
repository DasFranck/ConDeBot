#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
import json
import os

from config import OPS_FILE


# Check if user is op (NOT LOGGED FUNCTION, meant to be use in the source code of CDB)
def isop_user(user):
    nickdis = ""
    if (isinstance(user, str)):
        nickdis = user
    elif (isinstance(user, discord.User)):
        nickdis = get_nickdis(user)
    else:
        return (False)

    if (os.path.isfile(OPS_FILE)):
        with open(OPS_FILE) as ops_file:
            ops = json.load(ops_file)
        return (nickdis in ops)
    else:
        return (False)


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
