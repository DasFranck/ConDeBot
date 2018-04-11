#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from classes.Plugin import Plugin
from utilities import display_error

NAME = "Help"
DESCRIPTION = ""
USAGE = {}


class HelpPlugin(Plugin):
    def __init__(self, cdb):
        super().__init__(cdb)

        cdb.add_plugin_description(DESCRIPTION, NAME)
        cdb.add_plugin_usage(USAGE, NAME)

        cdb.reserve_keywords(["help"], "Help")

    async def on_message(self, message, cmd):
        if not cmd.triggered \
           or cmd.action not in ["help"]:
            return

        self.cdb.log_info_command("Help requested by " + str(cmd.author),
                                  message)

        if len(cmd.args) == 0:
            help_message = "**{} v{}**\nAvailable plugins:\n".format(self.cdb.NAME, self.cdb.VERSION)
            for plugin in self.cdb._plugin_metadata.keys():
                try:
                    help_message += "- {}: {}\n".format(plugin, self.cdb._plugin_metadata[plugin]["Description"])
                except KeyError:
                    help_message += "- {}: {}\n".format(plugin, "No description")
            help_message += "\n\nYou can access plugin's help by typing !help [plugin_name]"
        else:
            try:
                usage_node = self.cdb._plugin_metadata[cmd.args[0]]["Usage"]
                for arg in cmd.args[1:]:
                    usage_node = usage_node[arg]
                try:
                    help_message = usage_node["_"]
                except KeyError:
                    help_message = usage_node
            except KeyError:
                await display_error(self.cdb, cmd.channel, "No help is available for those arguments.")
                return

        await self.cdb.send_message(message.channel, help_message)
