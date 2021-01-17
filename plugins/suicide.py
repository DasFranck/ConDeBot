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
        if not cmd or not cmd.triggered:
            return

        if cmd.action in ["slain", "kill", "suicide"]:
            if not self.cdb.isop_user(message.author):
                await message.channel.send("You don't have the right to do that.")
                self.cdb.log_warn("Bot Suicide requested by NON-OP %s, FAILED" % str(cmd.author), message)
                return

            if (cmd.action == "slain"):
                await message.channel.send(f"{self.cdb.NAME} has been slained by {cmd.author}.")
            elif (cmd.action == "kill"):
                await message.channel.send(f"{self.cdb.NAME} has been killed by {cmd.author}.")
            elif (cmd.action == "suicide"):
                await message.channel.send("%s is suiciding himself. With %s's help." % (self.cdb.NAME, str(cmd.author)))

            self.cdb.log_info("Bot has been terminated by " + str(cmd.author), message)
            self.cdb.logger.info("#--------------END--------------#")

            # Trying to exit properly (client.py:494 from discord.py)
            await self.cdb.logout()

        if cmd.action in ["restart", "reboot"]:
            if not self.cdb.isop_user(message.author):
                await message.channel.send("You don't have the right to do that.")
                self.cdb.log_warn("Bot restart requested by NON-OP %s, FAILED" % str(cmd.author), message)
            else:
                await message.channel.send("Restart has been ordered by %s." % str(cmd.author))
                self.cdb.log_info("Bot has been restarted by " + str(cmd.author), message)
                self.cdb.logger.info("#------------RESTART------------#")
                await self.cdb.logout()
                sys.exit(30)
