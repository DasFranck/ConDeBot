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
        self.cdb.log_info("Source files requested by " + str(cmd.author), message)
        await message.channel.send(f"""{self.cdb.NAME}'s source files:
                                       https://git.dasfranck.fr/DasFranck/ConDeBot/
                                       https://github.com/DasFranck/ConDeBot/""")
