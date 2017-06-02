#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from classes.Plugin import Plugin
from utilities import isop_user, get_meta


class SuicidePlugin(Plugin):
    async def on_message(self, message):

        (msg, args, author, triggered, action) = get_meta(self.cdb, message)

        if (triggered and action in ["slain", "kill", "suicide"]):
            if not isop_user(message.author):
                await self.cdb.send_message(message.channel, "You don't have the right to do that.")
                self.cdb.logger.log_warn_command("Bot Suicide requested by NON-OP %s, FAILED" % (author), message)
            else:
                if (action == "slain"):
                    await self.cdb.send_message(message.channel, "%s has been slained by %s." % (self.cdb.NAME, author))
                elif (action == "kill"):
                    await self.cdb.send_message(message.channel, "%s has been killed by %s." % (self.cdb.NAME, author))
                elif (action == "suicide"):
                    await self.cdb.send_message(message.channel, "%s is suiciding himself. With %s's help." % (self.cdb.NAME, author))
                self.cdb.logger.log_info_command("Bot has been terminated by " + author, message)
                self.cdb.logger.logger.info("#--------------END--------------#")

                # Trying to exit properly (client.py:494 from discord.py)
                await self.cdb.logout()

        if (triggered and action in ["restart"]):
            if not isop_user(message.author):
                await self.cdb.send_message(message.channel, "You don't have the right to do that.")
                self.cdb.logger.log_warn_command("Bot Suicide requested by NON-OP %s, FAILED" % (author), message)
            else:
                await self.cdb.send_message(message.channel, "Restart has been ordered by %s." % author)
                await self.cdb.logout()
                sys.exit(30)
