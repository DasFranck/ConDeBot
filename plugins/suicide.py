#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from classes.Plugin import Plugin

NAME = "Suicide"
DESCRIPTION = "Remotly kill the bot"
USAGE = {}


class SuicidePlugin(Plugin):
    def __init__(self, cdb):
        super().__init__(cdb)
        cdb.reserve_keywords(["slain", "kill", "suicide", "restart", "reboot"], "Suicide")

    async def on_message(self, message, cmd):
        if not cmd \
           or not cmd.triggered:
            return

        if cmd.action in ["slain", "kill", "suicide"]:
            if not self.cdb.isop_user(message.author):
                await self.cdb.send_message(message.channel,
                                            "You don't have the right to do that.")
                self.cdb.log_warn_command("Bot Suicide requested by NON-OP %s, FAILED" % str(cmd.author), message)
                return

            if (cmd.action == "slain"):
                await self.cdb.send_message(message.channel,
                                            "%s has been slained by %s." % (self.cdb.NAME,
                                                                            str(cmd.author)))
            elif (cmd.action == "kill"):
                await self.cdb.send_message(message.channel,
                                            "%s has been killed by %s." % (self.cdb.NAME, str(cmd.author)))
            elif (cmd.action == "suicide"):
                await self.cdb.send_message(message.channel, "%s is suiciding himself. With %s's help." % (self.cdb.NAME, str(cmd.author)))

            self.cdb.log_info_command("Bot has been terminated by " + str(cmd.author), message)
            self.cdb.logger.info("#--------------END--------------#")

            # Trying to exit properly (client.py:494 from discord.py)
            await self.cdb.logout()

        if cmd.action in ["restart", "reboot"]:
            if not self.cdb.isop_user(message.author):
                await self.cdb.send_message(message.channel, "You don't have the right to do that.")
                self.cdb.log_warn_command("Bot restart requested by NON-OP %s, FAILED" % str(cmd.author), message)
            else:
                await self.cdb.send_message(message.channel, "Restart has been ordered by %s." % str(cmd.author))
                self.cdb.log_info_command("Bot has been restarted by " + str(cmd.author), message)
                self.cdb.logger.info("#------------RESTART------------#")
                await self.cdb.logout()
                sys.exit(30)
