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

    async def on_message(self, message, cmd):
        if not cmd.triggered \
           or cmd.action not in ["version"]:
            return

        self.cdb.log_info_command("Version requested by " + str(cmd.author),
                                  message)
        await self.cdb.send_message(message.channel,
                                    "{}'s version: {}\nDiscord API version :{}".format(
                                        self.cdb.NAME,
                                        self.cdb.VERSION,
                                        discord.__version__
                                    ))
