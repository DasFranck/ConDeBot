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

    async def on_message_edit(self, before, after):
        for plugin in self.plugins:
            self.loop.create_task(plugin.on_message_edit(before, after))

    async def on_message_delete(self, message):
        for plugin in self.plugins:
            self.loop.create_task(plugin.on_message_delete(message))

    async def on_channel_create(self, channel):
        for plugin in self.plugins:
            self.loop.create_task(plugin.on_channel_create(channel))

    async def on_channel_update(self, before, after):
        for plugin in self.plugins:
            self.loop.create_task(plugin.on_channel_update(before, after))

    async def on_channel_delete(self, channel):
        for plugin in self.plugins:
            self.loop.create_task(plugin.on_channel_delete(channel))

    async def on_member_join(self, member):
        for plugin in self.plugins:
            self.loop.create_task(plugin.on_member_join(member))

    async def on_member_remove(self, member):
        for plugin in self.plugins:
            self.loop.create_task(plugin.on_member_remove(member))

    async def on_member_update(self, before, after):
        for plugin in self.plugins:
            self.loop.create_task(plugin.on_member_update(before, after))

    async def on_server_join(self, server):
        for plugin in self.plugins:
            self.loop.create_task(plugin.on_server_join(server))

    async def on_server_update(self, before, after):
        for plugin in self.plugins:
            self.loop.create_task(plugin.on_server_update(before, after))

    async def on_server_role_create(self, server, role):
        for plugin in self.plugins:
            self.loop.create_task(plugin.on_server_role_create(server, role))

    async def on_server_role_delete(self, server, role):
        for plugin in self.plugins:
            self.loop.create_task(plugin.on_server_role_delete(server, role))

    async def on_server_role_update(self, server, role):
        for plugin in self.plugins:
            self.loop.create_task(plugin.on_server_role_update(server, role))

    async def on_voice_state_update(self, before, after):
        pass

    async def on_member_ban(self, member):
        for plugin in self.plugins:
            self.loop.create_task(plugin.on_member_ban(member))

    async def on_member_unban(self, member):
        for plugin in self.plugins:
            self.loop.create_task(plugin.on_member_unban(member))

    async def on_typing(self, channel, user, when):
        pass


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
