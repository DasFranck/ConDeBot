#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import namedtuple
import discord
import json
import os

from config.config import OPS_FILE


Command = namedtuple("Command",
                     # Message content and metadata
                     ["content",
                      "channel",
                      "timestamp",
                      "author",
                      "msg",  # Original Message Object reference

                      # Command parsing
                      "triggered",
                      "action",
                      "args"])


def isop_user(user_id):
    """ Check if user is op """
    if (os.path.isfile(OPS_FILE)):
        with open(OPS_FILE) as ops_file:
            ops = json.load(ops_file)
        return (user_id in ops)
    else:
        return (False)


def get_meta(cdb, message):
    """ Return a named tuple which contain metadata of a message """
    content = message.content
    args = content.split(" ")
    if (message.author == cdb.user or content is None or len(args[0]) == 0):
        return None

    if (cdb.PREF == ""):
        triggered = args[0][0] == "!"
        action = args[0][1:] if len(args[0]) > 0 else ""
        args = args[1:]
    else:
        triggered = args[0] == ("!" + cdb.PREF)
        action = content.split(" ")[1] if len(content.split(" ")) > 1 else ""
        args = args[2:]

    cmd = Command(message.content,
                  message.channel,
                  message.timestamp,
                  message.author,
                  message,
                  triggered,
                  action,
                  args)

    return cmd


async def display_error(cdb, channel, error_message, title="Error"):
    """ Display an error in an embed message """
    em = discord.Embed(title=title, description=error_message, colour=0xFF0000)
    await cdb.send_message(channel, embed=em)


async def display_warning(cdb, channel, error_message, title="Warning"):
    """ Display a warning in an embed message """
    em = discord.Embed(title=title, description=error_message, colour=0xFFCC00)
    await cdb.send_message(channel, embed=em)
