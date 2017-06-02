#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from classes.Plugin import Plugin
from utilities import get_meta


class SourcePlugin(Plugin):
    def __init__(self, cdb):
        super().__init__(cdb)

    async def on_message(self, message):
        (msg, args, author, triggered, action) = get_meta(self.cdb, message)
        if triggered and action in ["source"]:
            self.cdb.logger.log_info_command("Source files requested by " + author, message)
            await self.cdb.send_message(message.channel, self.cdb.NAME + "'s source files: \nhttps://git.dasfranck.fr/ConDeBot_Discord/\nhttps://github.com/DasFranck/ConDeBot_Discord")
            return
