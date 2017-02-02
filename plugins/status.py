#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord

from classes.Plugin import Plugin
from utilities import get_meta, isop_user


class StatusPlugin(Plugin):
    def __init__(self, cdb):
        super().__init__(cdb)
        self.status_dict = {"online": discord.Status.online,
                            "offline": discord.Status.offline,
                            "idle": discord.Status.idle,
                            "dnd": discord.Status.do_not_disturb,
                            "do_not_disturb": discord.Status.do_not_disturb,
                            "invisible": discord.Status.invisible}
        self.status = None
        self.game = None

    async def on_message(self, message):
        (msg, args, author, triggered, action) = get_meta(self.cdb, message)
        if not triggered:
            return

        if not isop_user(message.author):
            await self.cdb.send_message(message.channel, "You don't have the right to do that.")
            self.cdb.logger.log_warn_command("Changing bot status requested by NON-OP %s, FAILED" % (author), message)
        else:
            if action == "status":
                if len(args) == 0:
                    await self.cdb.send_message(message.channel, "Try with an argument for this command next time.")
                    await self.cdb.send_message(message.channel, "Valid arguments: online, offline, idle, dnd, invisible.")
                elif args[0].lower() in self.status_dict:
                    self.cdb.logger.log_info_command("Change bot's status to %s requested by %s" % (args[0].lower(), author), message)
                    self.status = self.status_dict[args[0].lower()]
                else:
                    await self.cdb.send_message(message.channel, "It's not a valid argument.")
                    await self.cdb.send_message(message.channel, "Valid arguments: online, offline, idle, dnd, invisible.")
            elif action == "game":
                if len(args) == 0:
                    self.game = None
                    self.cdb.logger.log_info_command("Erasing bot's game requested by %s" % (author), message)
                else:
                    self.game = discord.Game(name=message.content[6:])
                    self.cdb.logger.log_info_command("Change bot's game requested by %s" % (author), message)
            await self.cdb.change_presence(game=self.game, status=self.status)
