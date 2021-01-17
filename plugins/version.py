#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from classes.Plugin import Plugin
import discord

NAME = "Version"
DESCRIPTION = "Show CDB and Discord API Version"
USAGE = {}


class VersionPlugin(Plugin):
    def __init__(self, cdb):
        super().__init__(cdb)

        cdb.reserve_keywords(["version"], NAME)
        cdb.add_plugin_description(DESCRIPTION, NAME)
        cdb.add_plugin_usage(USAGE, NAME)

    async def on_message(self, message, cmd):
        if not cmd.triggered \
           or cmd.action not in ["version"]:
            return

        self.cdb.log_info_command("Version requested by %s" % str(cmd.author), message)
        await message.channel.send(f"{self.cdb.NAME}'s version: **{self.cdb.VERSION}**\nDiscord API version: **{discord.__version__}**")
