#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from classes.Plugin import Plugin


class SourcePlugin(Plugin):
    def __init__(self, cdb):
        super().__init__(cdb)

    async def on_message(self, message, cmd):
        if not cmd.triggered \
           or cmd.action not in ["source"]:
            return
        self.cdb.log_info_command("Source files requested by " + cmd.author_nickdis, message)
        await self.cdb.send_message(message.channel,
                                    ("{}'s source files:\n"
                                     "https://git.dasfranck.fr/ConDeBot_Discord/\n"
                                     "https://github.com/DasFranck/ConDeBot_Discord")
                                    .format(self.cdb.NAME))
        return
