#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Nothing here for now.
"""

# Setting up some strings globals
CDB_PATH = "./"
DESC = "ConDeBot - Un con de bot Discord"
NAME = "ConDeBot"
PREF = ""
SHME = "CDB"
VERS = "0.0.1b"

# Help message
# TODO: Should be automatically generated
HELP = "**" + NAME + " v" + VERS + "**\n```\nUSAGE :\n" \
            + "!coffee                  Serve some coffee\n"                                        \
            + "!kaamelott [-q ID]       Kaamelott quotes\n"                                         \
            + "!source                  Display an url to the bot's source code\n"                  \
            + "!version                 Show CDB and Discord API Version\n"                         \
            + "!op USERNAME             Grant USERNAME to Operator status (OP Rights needed)\n"     \
            + "!deop USERNAME           Remove USERNAME from Operator status (OP Rights needed)\n"  \
            + "!isop USERNAME           Check if USERNAME is an Operator status\n"                  \
            + "!op_list                 Print the Operators list\n"                                 \
            + "```"

# Import modules with try and catch
try:
    import argparse
    import discord
except ImportError as message:
    print("Missing package(s) for %s: %s" % (NAME, message))
    exit(12)

# Import classes
try:
    from classes import Logger
except ImportError as message:
    print("Missing python class(es) for %s: %s" % (NAME, message))
    exit(12)

# Import modules
try:
    from plugins import coffee
    from plugins import kaamelott
    from plugins import list
    from plugins import opmod
    from plugins import replier
    from plugins import suicide
    from plugins import status
    from plugins import utilities
except ImportError as message:
    print("Missing python module(s) for %s: %s" % (NAME, message))
    exit(12)

# Setting up client and logger as global
client = discord.Client()
logger = Logger.Logger()


# Triggered when the bot is ready
@client.async_event
def on_ready():
    user = client.user
    logger.logger.info("Sucessfully connected as %s (%s)" % (user.name, user.id))
    logger.logger.info("------------")
    return


# Triggered when the bot receive a message
@client.async_event
def on_message(message):
    msg = message.content
    args = msg.split(" ")
    if (message.author == client.user or msg is None or len(args[0]) == 0):
        return
    author = utilities.get_nickdis(message.author)
    chan = message.channel

    if (PREF == ""):
        triggered = args[0][0] == "!"
        action = args[0][1:] if len(args[0]) > 0 else ""
        args = args[1:]
    else:
        triggered = args[0] == ("!" + PREF)
        action = msg.split(" ")[1] if len(msg.split(" ")) > 1 else ""
        args = args[2:]

    # DO A MODULE POOL SOMEDAY. PLZ.
    if (triggered):
        if (action in ["help", ""]):
            logger.log_info_command("Help requested by " + author, message)
            yield from client.send_message(chan, HELP)

        elif action == "version":
            logger.log_info_command("Version requested by " + author, message)
            yield from client.send_message(chan, NAME + "'s version: " + VERS)

        elif action == "source":
            logger.log_info_command("Source files requested by " + author, message)
            yield from client.send_message(chan, NAME + "'s source files: https://git.daspat.fr/ConDeBot_Discord/")

        # Serve a delicious coffee (Module: "coffee")
        elif action in ["café", "cafe", "coffee"]:
            logger.log_info_command("Coffee requested by " + author, message)
            yield from client.send_message(chan, ":coffee:")
            yield from client.send_message(chan, coffee.coffee(client, logger, message, action, args, author))

        # Serve a delicious tea (Module: "coffee")
        elif action in ["thé", "the", "tea"]:
            logger.log_info_command("Tea requested by " + author, message)
            yield from client.send_message(chan, ":tea:")
            yield from client.send_message(chan, coffee.tea(client, logger, message, action, args, author))

        # Manage some kaamelott quotes (Module: "kaamelott")
        elif action in ["kaamelott"]:
            yield from kaamelott.main(client, logger, message, args, author)

        # Manage the death of this bot (Module: "suicide")
        elif action in ["slain", "kill", "suicide"]:
            yield from suicide.main(client, logger, message, action, args, author)

        # Manage operators (Module: "opmod")
        elif action in ["op", "deop", "isop", "op_list"]:
            yield from opmod.main(client, logger, message, action, args, author)

        # Display the commands call count (Module: "replier")
        elif action in ["count"]:
            yield from replier.count(client, logger, message, action, args, author)

        # Lock the permission to modify a specific trigger (Module: "replier")
        elif action in ["lock", "unlock"]:
            yield from replier.locker(client, logger, message, action, args, author)

        # Change the status/game of the bot (Module: "status")
        elif action in ["status", "game"]:
            yield from status.main(client, logger, message, action, args, author)

        # Pick a random element in a list and mange thoses lists (Module: "lists")
        elif action in ["list"]:
            yield from list.main(client, logger, message, action, args, author)

        elif action in ["triggerlist"]:
            yield from replier.list(client, logger, message, action, args, author)

        # If it's not a built-in command, check if it's related to replies (Module: "replier")
        else:
            yield from replier.main(client, logger, message, action, args, author)
    return


# The Main.
def main():
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument("token")
    args = parser.parse_args()

    client.run(args.token)
    return


if (__name__ == '__main__'):
    main()
