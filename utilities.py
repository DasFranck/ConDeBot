#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
import json
import os

from config.config import OPS_FILE


# Check if user is op
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


# Return a tuple which contain metadata of a message
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


# Display an error in an embed message
async def display_error(cdb, channel, error_message, title="Error"):
    em = discord.Embed(title=title, description=error_message, colour=0xFF0000)
    await cdb.send_message(channel, embed=em)


# Display a warning in an embed message
async def display_warning(cdb, channel, error_message, title="Warning"):
    em = discord.Embed(title=title, description=error_message, colour=0xFFCC00)
    await cdb.send_message(channel, embed=em)
