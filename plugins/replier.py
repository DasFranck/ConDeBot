#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
import os
import hjson

from classes.Plugin import Plugin
from config.config import REPLIES_FILE_DIR
from utilities import get_meta, isop_user


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
        if not os.path.isdir(REPLIES_FILE_DIR):
            os.makedirs(REPLIES_FILE_DIR)

    # Load the replies file into an array of dict
    async def load_replies(self, message, replies_path):
        if (os.path.isfile(replies_path)):
            with open(replies_path) as replies_file:
                try:
                    return hjson.load(replies_file)
                except:
                    self.cdb.logger.logger.error("JSON replies file loading failed.")
                    await self.cdb.send_message(message.channel, "The JSON replies file seems corrupted. Please fix it before using the replier module.")
                    return None
        else:
            return []

    # Print the number of times a message has been triggered
    async def count(self, message, action, args, author, replies):
        if (args is None or len(args) == 0):
            await self.cdb.send_message(message.channel, "Try with an argument for this command next time.")
            return
        else:
            for arg in args:
                reply = get_reply(replies, arg)
                if (reply is None):
                    self.cdb.logger.log_error_command("Count of non-existant trigger %s requested by %s" % (arg, author), message)
                    await self.cdb.send_message(message.channel, "The trigger %s doesn't even exist." % arg)
                else:
                    self.cdb.log_info_command("Count of trigger %s (%d) requested by %s" % (arg, reply["count"], author), message)
                    await self.cdb.send_message(message.channel, "The trigger %s has been called %d times." % (arg, reply["count"]))
        return

    # Send the list of the server's trigger messages
    async def list(self, message, action, args, author, replies):
        if message.server is None:
            await self.cdb.send_message(message.channel, "You can't use this command outside of a server for now.")
            return

        message_to_send = "Here's the list of triggers for {} ({})\n```".format(message.server.name, message.server.id)
        for reply in replies:
            message_to_send += reply["trigger"] + "\n"
        message_to_send += "```"
        await self.cdb.send_message(message.author, message_to_send)
        await self.cdb.send_message(message.channel, "{}: I've send you the trigger list by PM.".format(message.author.mention))
        self.cdb.logger.log_info_command("The trigger list has been requested by %s" % (author), message)
        return

    # Lock a reply (OP-ONLY)
    async def locker(self, message, action, args, author, replies, replies_path):
        if not isop_user(message.author):
            await self.cdb.send_message(message.channel, "You don't have the right to do that.")
            self.cdb.logger.log_warn_command("The trigger %s lock/unlock has been requested by NON-OP %s, FAILED" % (action if len(args) else "[ ERR ]", author), message)
            return
        else:
            if (args is None or len(args) == 0):
                await self.cdb.send_message(message.channel, "Try with an argument for this command next time.")
                return
            else:
                old_dict = get_reply(replies, args[0])
                if (old_dict is None):
                    return
                old_dict["locked"] = True if action == "lock" else False
                await self.cdb.send_message(message.channel, "Roger that, %s trigger has been %s." % (args[0], action + "ed"))
                self.cdb.logger.log_info_command("%s of trigger %s requested by %s" % (action.capitalize(), args[0], author), message)
                with open(replies_path, 'w') as replies_file:
                    hjson.dump(replies, replies_file, indent=' ' * 2)
        return

    async def replier(self, message, action, args, author, replies, replies_path):
        # Call the triggered message
        if (args is None or len(args) == 0 or args[0] == ">"):
            reply = get_reply(replies, action)
            if (reply is not None):
                if (args and args[0] == ">" and len(args) >= 2):
                    await self.cdb.send_message(message.channel, args[1] + ": " + reply["message"])
                else:
                    await self.cdb.send_message(message.channel, reply["message"])
                reply["count"] += 1
                self.cdb.logger.log_info_command("The trigger %s has been called by %s" % (action, author), message)
                with open(replies_path, 'w') as replies_file:
                    hjson.dump(replies, replies_file, indent=' ' * 2)
            else:
                pass
                # self.cdb.logger.log_info_command("Non-existant trigger %s has been called by %s" % (action, author), message)

        # Assign a message to this trigger
        elif (args[0] == "="):
            if (len(args) > 1):
                # Check if the reply dict already exist
                old_dict = get_reply(replies, action)
                # If the reply dict don't exist set it, else replace it
                if (old_dict is None):
                    new_dict = OrderedDict(trigger=action, message=" ".join(args[1:]), count=0, locked=False)
                    replies.append(new_dict)
                    self.cdb.logger.log_info_command("The new trigger %s has been set by %s" % (action, author), message)
                else:
                    # Check if the reply dict is locked
                    if (not isop_user(message.author) and "locked" in old_dict and old_dict["locked"] is True):
                        await self.cdb.send_message(message.channel, "Sorry, the %s trigger has been locked by an operator." % action)
                        self.cdb.logger.log_warn_command("The locked trigger %s reset has been requested by NON-OP %s, FAILED" % (action, author), message)
                        return
                    else:
                        old_dict["trigger"] = action
                        old_dict["message"] = " ".join(args[1:])
                        old_dict["count"] = 0
                        old_dict["locked"] = False
                        self.cdb.logger.log_info_command("The trigger %s has been reset by %s" % (action, author), message)
                await self.cdb.send_message(message.channel, "Roger that, %s trigger has been registered." % action)
                with open(replies_path, 'w') as replies_file:
                    hjson.dump(replies, replies_file, indent=' ' * 2)
            else:
                await self.cdb.send_message(message.channel, "You should try to put a message to assign to this trigger.")
                return
        return

    async def on_message(self, message):
        (msg, args, author, triggered, action) = get_meta(self.cdb, message)

        # Set file path
        if message.server is not None:
            replies_path = REPLIES_FILE_DIR + message.server.id + ".json"
        else:
            replies_path = REPLIES_FILE_DIR + "dump.json"

        # Load JSON replies file
        replies = await self.load_replies(message, replies_path)
        if (replies is None):
            return

        # Display the commands call count (Module: "replier")
        if triggered:
            if action in ["count"]:
                await self.count(message, action, args, author, replies)

            # Lock the permission to modify a specific trigger (Module: "replier")
            elif action in ["lock", "unlock"]:
                await self.locker(message, action, args, author, replies, replies_path)

            elif action in ["triggerlist"]:
                await self.list(message, action, args, author, replies)

            # If it's not a built-in command, check if it's related to replies (Module: "replier")
            else:
                await self.replier(message, action, args, author, replies, replies_path)
