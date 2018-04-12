#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re

import discord

from classes.Plugin import Plugin
from utilities import display_error, display_warning, display_success

NAME = "OpMod"
DESCRIPTION = "Manage operators"
USAGE = {
    "_": ("!opmod op: Add an user to the operator list [OP ONLY]"
          "!opmod deop: Remove an user from the operator list [OP ONLY]"
          "!opmod isop: Check if an user is an operator"
          "!opmod list: List every op on this server"
          "!opmod reload: Reload the op list from files [OP ONLY]"
          )
}


# Adding local channel moderator
# Should add checks for the id/mention input
# Need code review

class OpModPlugin(Plugin):
    def __init__(self, cdb):
        super().__init__(cdb)

        cdb.reserve_keywords(["opmod"], "OpMod")
        cdb.add_plugin_description(DESCRIPTION, NAME)
        cdb.add_plugin_usage(USAGE, NAME)

        if (os.path.isfile(self.cdb.OPS_FILE_PATH)):
            with open(self.cdb.OPS_FILE_PATH, encoding="utf8") as ops_file:
                self.ops = json.load(ops_file)
        else:
            self.ops = {"global": [], "channel": {}}

    def mention_to_user_id(self, mention):
        return re.sub('[<>!@]', '', mention)

    async def on_message(self, message, cmd):
        if not cmd.triggered \
           or cmd.action not in ["opmod"]:
            return

        # Display help here
        if (len(cmd.args) == 0):
            pass
        elif (cmd.args[0] in ["op", "add"]):
            await self.op_users(cmd)
        elif (cmd.args[0] in ["deop", "rm"]):
            await self.deop_users(cmd)
        elif (cmd.args[0] == "isop"):
            if (len(cmd.args) > 1):
                await self.isop(cmd)
            else:
                await self.isop_self(cmd)
        elif (cmd.args[0] == "list"):
            await self.op_list(cmd)
        elif (cmd.args[0] == "reload"):
            await self.reload_ops(cmd)
        else:
            # Display help
            pass

    async def isop(self, cmd):
        """
        Check if given users are op (LOGGED FUNCTION, meant to be used via !opmod isop "user_id" ...)
        """
        for arg in cmd.args[1:]:
            arg = self.mention_to_user_id(arg)

            self.cdb.log_info_command("Operator status of %s (%s) requested by %s" % (arg, self.cdb.isop_user(arg), str(cmd.author)), cmd.msg)
            if self.cdb.isop_user(arg):
                await self.cdb.send_message(cmd.channel, "%s is an operator." % discord.utils.get(cmd.msg.server.members, id=arg))
            else:
                await self.cdb.send_message(cmd.channel, "%s is not an operator." % discord.utils.get(cmd.msg.server.members, id=arg))

    async def isop_self(self, cmd):
        """
        Check if the user who called the command is op (LOGGED FUNCTION, meant to be used via !opmod isop)
        """
        self.cdb.log_info_command("Operator status of %s (%s) requested by %s" % (str(cmd.author), self.cdb.isop_user(cmd.author.id), str(cmd.author)), cmd.msg)
        if self.cdb.isop_user(cmd.author.id):
            await display_success(self.cdb, cmd.channel, "You are an operator.")
        else:
            await display_error(self.cdb, cmd.channel, "You are not an operator.")

    async def op_users(self, cmd, channel=None):
        """
        Add user(s) to the global moderators.
        """
        for arg in cmd.args[1:]:
            arg = self.mention_to_user_id(arg)

            if not self.cdb.isop_user(cmd.author.id):
                await display_error(self.cdb, cmd.channel, "You don't have the right to do that.")
                self.cdb.log_warn_command("Adding operator (%s) requested by NON-OP %s, FAILED" % (arg, str(cmd.author)), cmd.msg)
                return

            if self.cdb.isop_user(arg):
                await display_warning(self.cdb, cmd.channel, "%s is already an operator." % discord.utils.get(cmd.msg.server.members, id=arg))
                self.cdb.log_info_command("Adding operator (%s) requested by %s, failed cause he's already an operator" % (arg, str(cmd.author)), cmd.msg)
                continue

            self.ops["global"].append(arg)
            with open(self.cdb.OPS_FILE_PATH, 'w', encoding="utf8") as ops_file:
                json.dump(self.ops, ops_file)
            await display_success(self.cdb, cmd.channel, "%s has been added as operator." % discord.utils.get(cmd.msg.server.members, id=arg))
            self.cdb.log_info_command("Adding operator (%s) requested by %s, OK" % (arg, str(cmd.author)), cmd.msg)

        with open(self.cdb.OPS_FILE_PATH, 'w', encoding="utf8") as ops_file:
            json.dump(self.ops, ops_file)

    async def deop_users(self, cmd, channel=None):
        """
        Remove users from the global moderators.
        """
        for arg in cmd.args[1:]:
            arg = self.mention_to_user_id(arg)

            if not self.cdb.isop_user(cmd.author.id):
                await display_error(self.cdb, cmd.channel, "You don't have the right to do that.")
                self.cdb.log_warn_command("Deleting operator (%s) requested by NON-OP %s, FAILED" % (arg, str(cmd.author)), cmd.msg)
                return

            if not self.cdb.isop_user(arg):
                await display_warning(self.cdb, cmd.channel, "%s is already not an operator." % discord.utils.get(cmd.msg.server.members, id=arg))
                self.cdb.log_info_command("Deleting operator (%s) requested by %s, failed cause he's not an operator" % (arg, str(cmd.author)), cmd.msg)
                continue

            self.ops["global"].remove(arg)
            with open(self.cdb.OPS_FILE_PATH, 'w', encoding="utf8") as ops_file:
                json.dump(self.ops, ops_file)

            await display_success(self.cdb, cmd.channel, "%s has been removed from operator list." % discord.utils.get(cmd.msg.server.members, id=arg))
            self.cdb.log_info_command("Deleting operator (%s) requested by %s, OK" % (arg, str(cmd.author)), cmd.msg)

        with open(self.cdb.OPS_FILE_PATH, 'w', encoding="utf8") as ops_file:
            json.dump(self.ops, ops_file)

    async def op_list(self, cmd):
        """
        Display a list of global moderators.
        """
        string = "**Operator list:**\n"
        for op in self.ops["global"]:
            if (op is self.ops["global"][-1]):
                string += "- %s" % discord.utils.get(cmd.msg.server.members, id=op)
            else:
                string += "- %s\n" % discord.utils.get(cmd.msg.server.members, id=op)
        await self.cdb.send_message(cmd.channel, string)
        self.cdb.log_info_command("Operator list requested by %s" % str(cmd.author), cmd.msg)

    async def reload_ops(self, cmd):
        """
        Reload ops from the file at the path self.cdb.OPS_FILE_PATH
        """
        if not self.cdb.isop_user(cmd.author.id):
            await display_error(self.cdb, cmd.channel, "You don't have the right to do that.")
            self.cdb.log_warn_command("Reload operator file requested by NON-OP %s, FAILED" % str(cmd.author), cmd.msg)
            return

        if (os.path.isfile(self.cdb.OPS_FILE_PATH)):
            with open(self.cdb.OPS_FILE_PATH, encoding="utf8") as ops_file:
                self.ops = json.load(ops_file)
        else:
            self.ops = {"global": [], "channel": {}}
        self.cdb.log_info_command("Reload operator file requested by %s" % str(cmd.author), cmd.msg)
