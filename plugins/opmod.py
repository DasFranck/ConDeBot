#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re

import discord

from classes.Plugin import Plugin
from utilities import display_error, display_warning, display_success


# Should add checks for the id/mention input
# Need code review

class OpModPlugin(Plugin):
    def __init__(self, cdb):
        super().__init__(cdb)

    def mention_to_user_id(self, mention):
        return re.sub('[<>!@]', '', mention)

    async def on_message(self, message, cmd):
        if not cmd.triggered \
           or cmd.action not in ["op", "deop", "isop", "op_list"]:
            return

        # If json file exist, load it
        if (os.path.isfile(self.cdb.OPS_FILE_PATH)):
            with open(self.cdb.OPS_FILE_PATH, encoding="utf8") as ops_file:
                ops = json.load(ops_file)
        else:
            ops = []

        if (cmd.action == "op"):
            ops = await self.op_him(cmd, ops)
        elif (cmd.action == "deop"):
            ops = await self.deop_him(cmd, ops)
        elif (cmd.action == "isop"):
            if (len(cmd.args) > 0):
                await self.isop_l(cmd)
            else:
                await self.isop_s(cmd)
        elif (cmd.action == "op_list"):
            await self.op_list(cmd, ops)

        with open(self.cdb.OPS_FILE_PATH, 'w', encoding="utf8") as ops_file:
            json.dump(ops, ops_file)
        return

    # Check if user is op (LOGGED FUNCTION, meant to be used via !isop "nickdis")
    async def isop_l(self, cmd):
        for arg in cmd.args:
            arg = self.mention_to_user_id(arg)

            self.cdb.log_info_command("Operator status of %s (%s) requested by %s" % (arg, self.cdb.isop_user(arg), str(cmd.author)), cmd.msg)
            if self.cdb.isop_user(arg):
                await self.cdb.send_message(cmd.channel, "%s is an operator" % arg)
            else:
                await self.cdb.send_message(cmd.channel, "%s is not an operator" % arg)
        return

    # Check if user who called the command is op (LOGGED FUNCTION, meant to be used via !isop)
    async def isop_s(self, cmd):
        self.cdb.log_info_command("Operator status of %s (%s) requested by %s" % (str(cmd.author), self.cdb.isop_user(cmd.author.id), str(cmd.author)), cmd.msg)
        if self.cdb.isop_user(cmd.author.id):
            await self.cdb.send_message(cmd.channel, "You are an operator")
        else:
            await self.cdb.send_message(cmd.channel, "You are not an operator")
        return

    # Op user
    async def op_him(self, cmd, ops):
        for arg in cmd.args:
            arg = self.mention_to_user_id(arg)

            if not self.cdb.isop_user(cmd.author.id):
                await display_error(self.cdb, cmd.channel, "You don't have the right to do that.")
                self.cdb.log_warn_command("Adding operator (%s) requested by NON-OP %s, FAILED" % (arg, str(cmd.author)), cmd.msg)
                return (ops)

            if self.cdb.isop_user(arg):
                await display_warning(self.cdb, cmd.channel, "%s is already an operator" % discord.utils.get(cmd.msg.server.members, id=arg))
                self.cdb.log_info_command("Adding operator (%s) requested by %s, failed cause he's already an operator" % (arg, str(cmd.author)), cmd.msg)
                continue

            ops.append(arg)
            with open(self.cdb.OPS_FILE_PATH, 'w', encoding="utf8") as ops_file:
                json.dump(ops, ops_file)
            await display_success(self.cdb, cmd.channel, "%s has been added as operator" % discord.utils.get(cmd.msg.server.members, id=arg))
            self.cdb.log_info_command("Adding operator (%s) requested by %s, OK" % (arg, str(cmd.author)), cmd.msg)
        return (ops)

    # Deop user
    async def deop_him(self, cmd, ops):
        for arg in cmd.args:
            arg = self.mention_to_user_id(arg)

            if not self.cdb.isop_user(cmd.author.id):
                await display_error(self.cdb, cmd.channel, "You don't have the right to do that.")
                self.cdb.log_warn_command("Deleting operator (%s) requested by NON-OP %s, FAILED" % (arg, str(cmd.author)), cmd.msg)
                return (ops)

            if not self.cdb.isop_user(arg):
                await display_warning(self.cdb, cmd.channel, "%s is already not an operator" % discord.utils.get(cmd.msg.server.members, id=arg))
                self.cdb.log_info_command("Deleting operator (%s) requested by %s, failed cause he's not an operator" % (arg, str(cmd.author)), cmd.msg)
                continue

            with open(self.cdb.OPS_FILE_PATH, 'w', encoding="utf8") as ops_file:
                json.dump(ops, ops_file)
            ops.remove(arg)
            await display_success(self.cdb, cmd.channel, "%s has been removed from operator list" % discord.utils.get(cmd.msg.server.members, id=arg))
            self.cdb.log_info_command("Deleting operator (%s) requested by %s, OK" % (arg, str(cmd.author)), cmd.msg)
        return (ops)

    # Op user
    async def op_list(self, cmd, ops):
        string = "**Operator list:**\n"
        for op in ops:
            if (op is ops[-1]):
                string += "- %s" % discord.utils.get(cmd.msg.server.members, id=op)
            else:
                string += "- %s\n" % discord.utils.get(cmd.msg.server.members, id=op)
        await self.cdb.send_message(cmd.channel, string)
        self.cdb.log_info_command("Operator list requested by %s" % str(cmd.author), cmd.msg)
        return
