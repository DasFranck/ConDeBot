#!/usr/bin/python3

import argparse
import json
import os

# sys.path.insert(0, "lib")
import discord

from classes.PluginManager import PluginManager
from classes.Logger import Logger
from config import config
from utilities import get_meta


class ConDeBot(discord.Client):
    def __init__(self, *args, **kwargs):
        self.NAME = config.NAME
        self.SHME = config.SHORT_NAME
        self.DESC = config.DESCRIPTION
        self.PREF = config.CMD_PREFIX
        self.DATA_PATH = config.DATA_PATH
        self.OPS_FILE_PATH = config.DATA_PATH + "/ops.json"
        self.CDB_PATH = "./"
        self.VERSION = "1.1"

        self._reserved_keywords = {}
        self._plugin_metadata = {}

        super().__init__(*args, **kwargs)

        self.logger = Logger()
        self.plugins = []
        self.plugin_manager = PluginManager(self)
        self.plugin_manager.load_all()

    def add_plugin_metadata(self, metaname, metadata, plugin_name):
        try:
            self._plugin_metadata[plugin_name][metaname] = metadata
        except KeyError:
            self._plugin_metadata[plugin_name] = {metaname: metadata}

    def add_plugin_usage(self, usage, plugin_name):
        self.add_plugin_metadata("Usage", usage, plugin_name)

    def add_plugin_description(self, description, plugin_name):
        self.add_plugin_metadata("Description", description, plugin_name)

    def reserve_keyword(self, keyword, plugin_name):
        """ Manage reserved keywords """
        if keyword not in self._reserved_keywords:
            self._reserved_keywords[keyword] = [plugin_name]
        else:
            print("Warning: Conflicting with the plugins {} for the keyword {}".format(self._reserved_keywords[keyword], keyword))
            self._reserved_keywords[keyword].append(plugin_name)
        pass

    def unreserve_keyword(self, keyword):
        del self._reserved_keywords[keyword]

    def reserve_keywords(self, keyword_list, plugin_name):
        for keyword in keyword_list:
            self.reserve_keyword(keyword, plugin_name)

    def unreserve_keywords(self, keyword_list):
        for keyword in keyword_list:
            self.unreserve_keyword(keyword)

    # Aliases to self.logger functions
    def log_error_command(self, *args, **kwargs):
        self.logger.log_error_command(*args, **kwargs)

    def log_warn_command(self, *args, **kwargs):
        self.logger.log_warn_command(*args, **kwargs)

    def log_info_command(self, *args, **kwargs):
        self.logger.log_info_command(*args, **kwargs)

    async def on_ready(self):
        """Triggered when the bot is ready"""
        self.logger.info("Sucessfully connected as %s (%s)" % (self.user.name,
                                                               self.user.id))
        self.logger.info("------------")

    async def on_message(self, message):
        cmd = get_meta(self, message)
        if not cmd:
            return
        for plugin in self.plugins:
            self.loop.create_task(plugin.on_message(message, cmd))

    # async def on_message_edit(self, before, after):
    #     for plugin in self.plugins:
    #         self.loop.create_task(plugin.on_message_edit(before, after))

    # async def on_message_delete(self, message):
    #     for plugin in self.plugins:
    #         self.loop.create_task(plugin.on_message_delete(message))

    # async def on_reaction_add(self, reaction, user):
    #     for plugin in self.plugins:
    #         self.loop.create_task(plugin.on_reaction_add(reaction, user))

    # async def on_reaction_remove(self, reaction, user):
    #     for plugin in self.plugins:
    #         self.loop.create_task(plugin.on_reaction_remove(reaction, user))

    # async def on_reaction_clear(self, message, reactions):
    #     for plugin in self.plugins:
    #         self.loop.create_task(plugin.on_reaction_clear(message, reactions))

    # async def on_member_join(self, member):
    #     for plugin in self.plugins:
    #         self.loop.create_task(plugin.on_member_join(member))

    # async def on_member_remove(self, member):
    #     for plugin in self.plugins:
    #         self.loop.create_task(plugin.on_member_remove(member))

    # async def on_member_update(self, before, after):
    #     for plugin in self.plugins:
    #         self.loop.create_task(plugin.on_member_update(before, after))

    # async def on_guild_join(self, guild):
    #     for plugin in self.plugins:
    #         self.loop.create_task(plugin.on_guild_join(guild))

    # async def on_guild_remove(self, guild):
    #     for plugin in self.plugins:
    #         self.loop.create_task(plugin.on_guild_remove(guild))

    # async def on_guild_update(self, before, after):
    #     for plugin in self.plugins:
    #         self.loop.create_task(plugin.on_guild_update(before, after))

    # async def on_guild_role_create(self, guild, role):
    #     for plugin in self.plugins:
    #         self.loop.create_task(plugin.on_guild_role_create(guild, role))

    # async def on_guild_role_delete(self, guild, role):
    #     for plugin in self.plugins:
    #         self.loop.create_task(plugin.on_guild_role_delete(guild, role))

    # async def on_guild_role_update(self, guild, role):
    #     for plugin in self.plugins:
    #         self.loop.create_task(plugin.on_guild_role_update(guild, role))

    # async def on_voice_state_update(self, member, before, after):
    #     pass

    # async def on_member_ban(self, guild, member):
    #     for plugin in self.plugins:
    #         self.loop.create_task(plugin.on_member_ban(member))

    # async def on_member_unban(self, member):
    #     for plugin in self.plugins:
    #         self.loop.create_task(plugin.on_member_unban(member))

    # async def on_typing(self, channel, user, when):
    #     pass

    def isop_user(self, user_id):
        """ Check if user is op """
        if (os.path.isfile(self.OPS_FILE_PATH)):
            with open(self.OPS_FILE_PATH, encoding="utf8") as ops_file:
                ops = json.load(ops_file)
            return (ops["global"] and user_id in ops["global"])
        else:
            return (False)


# The Main.
def main():
    cdb = ConDeBot()

    parser = argparse.ArgumentParser()
    parser.add_argument("--token")
    args = parser.parse_args()

    cdb.run(args.token)


if (__name__ == '__main__'):
    main()
