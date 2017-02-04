#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from classes.Plugin import Plugin
from utilities import get_meta


class VersionPlugin(Plugin):
    def __init__(self, cdb):
        super().__init__(cdb)

    async def on_message(self, message):
        (msg, args, author, triggered, action) = get_meta(self.cdb, message)
        if triggered and action in "version":
            self.cdb.logger.log_info_command("Version requested by " + author, message)
            await self.cdb.send_message(message.channel, self.cdb.NAME + "'s version: " + self.cdb.VERS)
            return
