#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Nothing here for now.
"""

# Setting up some strings globals
CDB_PATH = "./"
DESC = "ConDeBot - Un con de bot Discord"
NAME = "ConDeBot"
SHME = "CDB"
TOKEN = "MjIzMDg4MDIyNjU1MjA1Mzc2.CrG2dQ.1fJEF1N_vVTtAah7obDe5BwQAl"
VERS = "0.0.1a"


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
    print("Missing python class(s) for %s: %s" % (NAME, message))
    exit(12)

# Import modules
try:
    from modules import coffee
    from modules import kaamelott
except ImportError as message:
    print("Missing python module(s) for %s: %s" % (NAME, message))
    exit(12)

# Setting up client as global
client = discord.Client()
logger = Logger.Logger()


# Trigger when the bot is ready
@client.async_event
def on_ready():
    user = client.user
    logger.logger.info("Sucessfully connected as %s (%s)" % (user.name, user.id))
    logger.logger.info("------------")
    return


# Trigger when the bot receive a message on a channel only (No PM)
@client.async_event
def on_message(message):
    if (message.author == client.user):
        return
    nick = message.author.name
    msg = message.content
    chan = message.channel
    action = msg.split(" ")[1] if len(msg.split(" ")) > 1 else ""

    if (msg.split(" ")[0] == "!cdb"):
        if (action in ["help", ""]):
            logger.log_info_command("Help requested by " + nick, message)
            yield from client.send_message(chan, "You asked for help %s?" % nick)

        elif (action == "version"):
            logger.log_info_command("Version requested by " + nick, message)
            yield from client.send_message(chan, "You asked for my version %s?" % nick)

        elif (action == "source"):
            logger.log_info_command("Source files requested by " + nick, message)
            yield from client.send_message(chan, "Well, my creator is a douche and has still not put my source code on internet")

        # Serve a delicious coffee (Module: "coffee")
        elif (action in ["café", "cafe", "coffee"]):
            logger.log_info_command("Coffee requested by " + nick, message)
            yield from client.send_message(chan, coffee.quote(nick))

        elif (action in ["kaamelott"]):
            kaamelott.main(client, logger, message, msg, nick)
    return


# The Main.
def main():
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument("--token", default=TOKEN)
    args = parser.parse_args()

    client.run(args.token)
    return


if __name__ == '__main__':
    main()
