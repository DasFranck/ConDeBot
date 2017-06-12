#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from classes.Plugin import Plugin
from utilities import get_meta


class SourcePlugin(Plugin):
    def __init__(self, cdb):
        super().__init__(cdb)

    async def on_message(self, message):
        cmd = get_meta(self.cdb, message)
        if cmd.triggered and cmd.action in ["source"]:
            self.cdb.logger.log_info_command("Source files requested by " + cmd.author_nickdis, message)
            await self.cdb.send_message(message.channel,
                                        ("{}'s source files:\n",
                                         "https://git.dasfranck.fr/ConDeBot_Discord/\n"
                                         "https://github.com/DasFranck/ConDeBot_Discord")
                                        .format(self.CDB.name))
            return
