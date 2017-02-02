#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import os

from config import OPS_FILE, OPS_FILE_PATH
from classes.Plugin import Plugin
from utilities import isop_user, get_meta


class OpModPlugin(Plugin):
    def __init__(self, cdb):
        super().__init__(cdb)
        if (not os.path.exists(OPS_FILE_PATH)):
            os.makedirs(OPS_FILE_PATH)

    async def on_message(self, message):
        (msg, args, author, triggered, action) = get_meta(self.cdb, message)
        if not triggered or action not in ["op", "deop", "isop", "op_list"]:
            return

        ops = []
        # If json file exist, load it
        if (os.path.isfile(OPS_FILE)):
            with open(OPS_FILE) as ops_file:
                ops = json.load(ops_file)

        if (action == "op"):
            for arg in args:
                ops = await self.op_him(message, author, arg, ops)
        elif (action == "deop"):
            for arg in args:
                ops = await self.deop_him(message, author, arg, ops)
        elif (action == "isop"):
            if (len(args) == 0):
                await self.isop_s(message, author)
            else:
                for arg in args:
                    await self.isop_l(message, author, arg)
        elif (action == "op_list"):
            await self.op_list(message, author, ops)

        with open(OPS_FILE, 'w') as ops_file:
            json.dump(ops, ops_file)
        return

    # Check if user is op (LOGGED FUNCTION, meant to be used via !isop "nickdis")
    async def isop_l(self, message, author, arg):
        self.cdb.logger.log_info_command("Operator status of %s (%s) requested by %s" % (arg, await isop_user(arg), author), message)
        if isop_user(arg):
            await self.cdb.send_message(message.channel, "%s is an operator" % arg)
        else:
            await self.cdb.send_message(message.channel, "%s is not an operator" % arg)
        return

    # Check if user who called the command is op (LOGGED FUNCTION, meant to be used via !isop)
    async def isop_s(self, message, author):
        self.cdb.logger.log_info_command("Operator status of %s (%s) requested by %s" % (message.author, await isop_user(message.author), author), message)
        if isop_user(message.author):
            await self.cdb.send_message(message.channel, "You are an operator")
        else:
            await self.cdb.send_message(message.channel, "You are not an operator")
        return

    # Op user
    async def op_him(self, message, author, arg, ops):
        if not isop_user(message.user):
            await self.cdb.send_message(message.channel, "You don't have the right to do that.")
            self.cdb.logger.log_warn_command("Adding operator (%s) requested by NON-OP %s, FAILED" % (arg, author), message)
            return (ops)

        if isop_user(arg):
            await self.cdb.send_message(message.channel, "%s is already an operator" % arg)
            self.cdb.logger.log_info_command("Adding operator (%s) requested by %s, failed cause he's already an operator" % (arg, author), message)
            return (ops)

        ops.append(arg)
        with open(OPS_FILE, 'w') as ops_file:
            json.dump(ops, ops_file)
        await self.cdb.send_message(message.channel, "%s has been added as operator" % arg)
        self.cdb.logger.log_info_command("Adding operator (%s) requested by %s, OK" % (arg, author), message)
        return (ops)

    # Deop user
    async def deop_him(self, message, author, arg, ops):
        if not isop_user(message.user):
            await self.cdb.send_message(message.channel, "You don't have the right to do that.")
            self.cdb.logger.log_warn_command("Deleting operator (%s) requested by NON-OP %s, FAILED" % (arg, author), message)
            return (ops)

        if not isop_user(arg):
            await self.cdb.send_message(message.channel, "%s is already not an operator" % arg)
            self.cdb.logger.log_info_command("Deleting operator (%s) requested by %s, failed cause he's not an operator" % (arg, author), message)
            return (ops)

        with open(OPS_FILE, 'w') as ops_file:
            json.dump(ops, ops_file)
        ops.remove(arg)
        await self.cdb.send_message(message.channel, "%s has been removed from operator list" % arg)
        self.cdb.logger.log_info_command("Deleting operator (%s) requested by %s, OK" % (arg, author), message)
        return (ops)

    # Op user
    async def op_list(self, message, author, ops):
        string = "Operator list:\n"
        for op in ops:
            if (op is ops[-1]):
                string += "%s" % op
            else:
                string += "%s, " % op
        await self.cdb.send_message(message.channel, string)
        self.cdb.logger.log_info_command("Operator list requested by %s" % author, message)
        return
