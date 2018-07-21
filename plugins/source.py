#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from classes.Plugin import Plugin

NAME = "Source"
DESCRIPTION = "Display an url to the bot's source code"
USAGE = {}


class SourcePlugin(Plugin):
    def __init__(self, cdb):
        super().__init__(cdb)

        cdb.add_plugin_description(DESCRIPTION, NAME)
        cdb.add_plugin_usage(USAGE, NAME)
        cdb.reserve_keywords(["source"], NAME)

    async def on_message(self, message, cmd):
        if (not cmd.triggered 
            or cmd.action not in ["source"]):
            return
        self.cdb.log_info_command("Source files requested by " + str(cmd.author), message)
        await self.cdb.send_message(message.channel,
                                    ("{}'s source files:\n"
                                     "https://git.dasfranck.fr/ConDeBot/\n"
                                     "https://github.com/DasFranck/ConDeBot/")
                                    .format(self.cdb.NAME))
        return
