#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord

from classes.Plugin import Plugin

NAME = "Status"
DESCRIPTION = "Change the bot status and his played game on discord"
USAGE = {}


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

        cdb.reserve_keywords(["status", "game"], "Status")
        cdb.add_plugin_description(DESCRIPTION, NAME)
        cdb.add_plugin_usage(USAGE, NAME)

    async def on_message(self, message, cmd):
        if not cmd.triggered \
           or cmd.action not in ["status", "game"]:
            return

        if not self.cdb.isop_user(message.author):
            await self.cdb.send_message(message.channel, "You don't have the right to do that.")
            self.cdb.log_warn_command("Changing bot status requested by NON-OP %s, FAILED" % (str(cmd.author)), message)
        else:
            if cmd.action == "status":
                if len(cmd.args) == 0:
                    await self.cdb.send_message(message.channel, "Try with an argument for this command next time.")
                    await self.cdb.send_message(message.channel, "Valid arguments: online, offline, idle, dnd, invisible.")
                elif cmd.args[0].lower() in self.status_dict:
                    self.cdb.log_info_command("Change bot's status to %s requested by %s" % (cmd.args[0].lower(), str(cmd.author)), message)
                    self.status = self.status_dict[cmd.args[0].lower()]
                else:
                    await self.cdb.send_message(message.channel, "It's not a valid argument.")
                    await self.cdb.send_message(message.channel, "Valid arguments: online, offline, idle, dnd, invisible.")
            elif cmd.action == "game":
                if len(cmd.args) == 0:
                    self.game = None
                    self.cdb.log_info_command("Erasing bot's game requested by %s" % (str(cmd.author)), message)
                else:
                    self.game = discord.Game(name=message.content[6:])
                    self.cdb.log_info_command("Change bot's game requested by %s" % (str(cmd.author)), message)
            await self.cdb.change_presence(game=self.game, status=self.status)
