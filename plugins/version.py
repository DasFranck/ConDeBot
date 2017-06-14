#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from classes.Plugin import Plugin


class VersionPlugin(Plugin):
    def __init__(self, cdb):
        super().__init__(cdb)

    async def on_message(self, message, cmd):
        if not cmd.triggered \
           or cmd.action not in ["version"]:
            return

        self.cdb.logger.log_info_command("Version requested by " + cmd.author_nickdis,
                                         message)
        await self.cdb.send_message(message.channel,
                                    "{}'s version: {}".format(
                                        self.cdb.NAME,
                                        self.cdb.VERS
                                    ))
        return
