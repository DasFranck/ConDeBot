#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Help message
# TODO: Should be automatically generated
# HELP = "**" + NAME + " v" + VERS + "**\n```\nUSAGE :\n" \
#            + "!coffee                  Serve some coffee\n"                                        \
#            + "!kaamelott [-q ID]       Kaamelott quotes\n"                                         \
#            + "!source                  Display an url to the bot's source code\n"                  \
#            + "!version                 Show CDB and Discord API Version\n"                         \
#            + "!op USERNAME             Grant USERNAME to Operator status (OP Rights needed)\n"     \
#            + "!deop USERNAME           Remove USERNAME from Operator status (OP Rights needed)\n"  \
#            + "!isop USERNAME           Check if USERNAME is an Operator status\n"                  \
#            + "!op_list                 Print the Operators list\n"                                 \
#            + "```"

# Import modules with try and catch
import argparse
import discord

from classes.PluginManager import PluginManager
from classes.Logger import Logger

from config import NAME, SHORT_NAME, DESCRIPTION, CMD_PREFIX


class ConDeBot(discord.Client):
    def __init__(self, *args, **kwargs):
        self.NAME = NAME
        self.SHME = SHORT_NAME
        self.DESC = DESCRIPTION
        self.PREF = CMD_PREFIX

        self.CDB_PATH = "./"
        self.VERS = "0.0.1b"

        super().__init__(*args, **kwargs)
        self.logger = Logger()
        self.plugin_manager = PluginManager(self)
        self.plugin_manager.load_all()

    # Triggered when the bot is ready
    async def on_ready(self):
        self.logger.logger.info("Sucessfully connected as %s (%s)" % (self.user.name, self.user.id))
        self.logger.logger.info("------------")
        return

    # Triggered when the bot receive a message
    async def on_message(self, message):
        for plugin in self.plugins:
            self.loop.create_task(plugin.on_message(message))
        print("GUD")

#        # DO A MODULE POOL SOMEDAY. PLZ.
#        if (triggered):
#            if (action in ["help", ""]):
#                self.logger.log_info_command("Help requested by " + author, message)
#                await self.send_message(chan, HELP)
#
#            elif action == "version":
#                self.logger.log_info_command("Version requested by " + author, message)
#                await self.send_message(chan, NAME + "'s version: " + VERS)
#
#            elif action == "source":
#                self.logger.log_info_command("Source files requested by " + author, message)
#                await self.send_message(chan, NAME + "'s source files: https://git.daspat.fr/ConDeBot_Discord/")
#
#            # Display the commands call count (Module: "replier")
#            elif action in ["count"]:
#                await replier.count(self, self.logger, message, action, args, author)
#
#            # Lock the permission to modify a specific trigger (Module: "replier")
#            elif action in ["lock", "unlock"]:
#                await replier.locker(self, self.logger, message, action, args, author)
#
#            # Pick a random element in a list and mange thoses lists (Module: "lists")
#            elif action in ["list"]:
#                await list.main(self, self.logger, message, action, args, author)
#
#            elif action in ["triggerlist"]:
#                await replier.list(self, self.logger, message, action, args, author)
#
#            # If it's not a built-in command, check if it's related to replies (Module: "replier")
#            else:
#                await replier.main(self, self.logger, message, action, args, author)
#        return


# The Main.
def main():
    cdb = ConDeBot()

    parser = argparse.ArgumentParser()
    parser.add_argument("token")
    args = parser.parse_args()

    cdb.run(args.token)
    return


if (__name__ == '__main__'):
    main()
