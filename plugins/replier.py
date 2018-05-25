#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
import os
import hjson

from classes.Plugin import Plugin

NAME = "REPLIER"
DESCRIPTION = "Register custom replies for the bot"
USAGE = {}


# Get the reply dict assign to the trigger
def get_reply(replies, trigger):
    if (replies is None):
        return None
    for reply in replies:
        if (reply["trigger"] == trigger):
            return reply
    return None


class ReplierPlugin(Plugin):
    def __init__(self, cdb):
        super().__init__(cdb)

        self.REPLIER_DIR_PATH = self.cdb.DATA_PATH + "replier/"
        os.makedirs(self.REPLIER_DIR_PATH, exist_ok=True)

        cdb.add_plugin_description(DESCRIPTION, NAME)
        cdb.add_plugin_usage(USAGE, NAME)

    async def load_replies(self, cmd, replies_path):
        """ Load the replies file into an array of dict """
        if (os.path.isfile(replies_path)):
            with open(replies_path, encoding="utf8") as replies_file:
                try:
                    return hjson.load(replies_file, encoding="utf8")
                except:
                    self.cdb.logger.error("JSON replies file loading failed.")
                    await self.cdb.send_message(cmd.msg.channel, "The JSON replies file seems corrupted. Please fix it before using the replier module.")
                    return None
        else:
            return []

    async def count(self, cmd, replies):
        """ Print the number of times a message has been triggered"""
        if (cmd.args is None or len(cmd.args) == 0):
            await self.cdb.send_message(cmd.msg.channel,
                                        "Try with an argument for this command next time.")
            return

        for arg in cmd.args:
            reply = get_reply(replies, arg)
            if (reply is None):
                self.cdb.log_error_command("Count of non-existant trigger %s requested by %s" % (arg,
                                                                                                 str(cmd.author)),
                                           cmd.msg)
                await self.cdb.send_message(cmd.msg.channel,
                                            "The trigger %s doesn't even exist." % arg)
            else:
                self.cdb.log_info_command("Count of trigger %s (%d) requested by %s" % (arg,
                                                                                        reply["count"],
                                                                                        str(cmd.author)),
                                          cmd.msg)
                await self.cdb.send_message(cmd.msg.channel,
                                            "The trigger %s has been called %d times." % (arg,
                                                                                          reply["count"]))

    async def list(self, cmd, replies):
        """ Send the list of the server's trigger messages to the requester"""
        if cmd.msg.server is None:
            await self.cdb.send_message(cmd.msg.channel,
                                        "You can't use this command outside of a server for now.")
            return

        message_to_send = "Here's the list of triggers for {} ({})\n```".format(cmd.msg.server.name,
                                                                                cmd.msg.server.id)
        for reply in replies:
            message_to_send += reply["trigger"] + "\n"
        message_to_send += "```"
        await self.cdb.send_message(cmd.msg.author, message_to_send)
        await self.cdb.send_message(cmd.msg.channel,
                                    "{}: I've send you the trigger list by PM.".format(cmd.msg.author.mention))
        self.cdb.log_info_command("The trigger list has been requested by %s" % (str(cmd.author)), cmd.msg)
        return

    async def locker(self, cmd, replies, replies_path):
        """ Unlock/Lock a reply (OP-ONLY) """
        if not self.cdb.isop_user(cmd.msg.author.id):
            await self.cdb.send_message(cmd.msg.channel,
                                        "You don't have the right to do that.")
            self.cdb.log_warn_command("The trigger %s lock/unlock has been requested by NON-OP %s, FAILED"
                                      % (cmd.action if len(cmd.args) else "[ ERR ]", str(cmd.author)),
                                      cmd.msg)
            return

        if (cmd.args is None or len(cmd.args) == 0):
            await self.cdb.send_message(cmd.msg.channel, "Try with an argument for this command next time.")
            return

        old_dict = get_reply(replies, cmd.args[0])
        if (old_dict is None):
            return

        old_dict["locked"] = True if cmd.action == "lock" else False
        await self.cdb.send_message(cmd.msg.channel, "Roger that, %s trigger has been %s." % (cmd.args[0], cmd.action + "ed"))
        self.cdb.log_info_command("%s of trigger %s requested by %s" % (cmd.action.capitalize(), cmd.args[0], str(cmd.author)), cmd.msg)
        with open(replies_path, 'w', encoding="utf8") as replies_file:
            hjson.dump(replies, replies_file, indent=' ' * 2, encoding="utf8")

    async def replier(self, message, action, args, author, replies, replies_path):
        """ Call the triggered message """
        if action in self.cdb._reserved_keywords:
            return

        if (args is None or len(args) == 0 or args[0] == ">"):
            reply = get_reply(replies, action)
            if (reply is not None):
                if (args and args[0] == ">" and len(args) >= 2):
                    await self.cdb.send_message(message.channel, args[1] + ": " + reply["message"])
                else:
                    await self.cdb.send_message(message.channel, reply["message"])
                reply["count"] += 1
                self.cdb.log_info_command("The trigger %s has been called by %s" % (action, author), message)
                with open(replies_path, 'w', encoding="utf8") as replies_file:
                    hjson.dump(replies, replies_file, indent=' ' * 2, encoding="utf8")
            else:
                pass
                # self.cdb.log_info_command("Non-existant trigger %s has been called by %s" % (action, author), message)

        elif (args[0] == "<"):
            if (len(args) > 1):
                return

        # Assign a message to this trigger
        elif (args[0] == "="):
            if (len(args) > 1):
                # Check if the reply dict already exist
                old_dict = get_reply(replies, action)
                # If the reply dict don't exist set it, else replace it
                if (old_dict is None):
                    new_dict = OrderedDict(trigger=action, message=" ".join(args[1:]), count=0, locked=False)
                    replies.append(new_dict)
                    self.cdb.log_info_command("The new trigger %s has been set by %s" % (action, author), message)
                else:
                    # Check if the reply dict is locked
                    if (not self.cdb.isop_user(message.author) and "locked" in old_dict and old_dict["locked"] is True):
                        await self.cdb.send_message(message.channel, "Sorry, the %s trigger has been locked by an operator." % action)
                        self.cdb.log_warn_command("The locked trigger %s reset has been requested by NON-OP %s, FAILED" % (action, author), message)
                        return
                    else:
                        old_dict["trigger"] = action
                        old_dict["message"] = " ".join(args[1:])
                        old_dict["count"] = 0
                        old_dict["locked"] = False
                        self.cdb.log_info_command("The trigger %s has been reset by %s" % (action, author), message)
                await self.cdb.send_message(message.channel, "Roger that, %s trigger has been registered." % action)
                with open(replies_path, 'w', encoding="utf8") as replies_file:
                    hjson.dump(replies, replies_file, indent=' ' * 2, encoding="utf8")
            else:
                await self.cdb.send_message(message.channel, "You should try to put a message to assign to this trigger.")
                return
        return

    async def on_message(self, message, cmd):
        if not cmd or not cmd.triggered:
            return

        # Set file path
        if message.server is not None:
            replies_path = self.REPLIER_DIR_PATH + message.server.id + ".json"
        else:
            replies_path = self.REPLIER_DIR_PATH + "dump.json"

        # Load JSON replies file
        replies = await self.load_replies(cmd, replies_path)
        if (replies is None):
            return

        # Display the commands call count (Module: "replier")
        if cmd.action in ["count"]:
            await self.count(cmd, replies)

        # Lock the permission to modify a specific trigger (Module: "replier")
        elif cmd.action in ["lock", "unlock"]:
            await self.locker(cmd, replies, replies_path)

        elif cmd.action in ["triggerlist"]:
            await self.list(cmd, replies)

        # If it's not a built-in command, check if it's related to replies (Module: "replier")
        else:
            await self.replier(message, cmd.action, cmd.args, str(cmd.author), replies, replies_path)
