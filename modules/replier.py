#!/usr/bin/env python3
# -*- coding: utf-8 -*-

REPLIES_FILE_PATH = "jsonfiles/"
REPLIES_FILE = REPLIES_FILE_PATH + "replies.json"

try:
    from collections import OrderedDict
    from modules import opmod
    import os
    import hjson
except ImportError as message:
    print("Missing package(s) for the replier module: %s" % message)
    exit(12)

# TODO : ADD LOGGING FUNCTION CALL


# Lock a reply (OP-ONLY)
async def lock(client, logger, message, action, args, author):
    if (not await opmod.isop_user(message.author)):
        await client.send_message(message.channel, "You don't have the right to do that.")
        logger.log_warn_command("Bot Suicide requested by NON-OP %s, FAILED" % (author), message)
    else:
        print()


# Get the reply dict assign to the trigger
def get_reply(replies, trigger):
    if (replies is None):
        return None
    for reply in replies:
        if (reply["trigger"] == trigger):
            return reply
    return None


# Load the replies file into an array of dict
async def load_replies(client, message):
    if (os.path.isfile(REPLIES_FILE)):
        with open(REPLIES_FILE) as replies_file:
            try:
                return hjson.load(replies_file)
            except:
                await client.send_message(message.channel, "The JSON replies file seems corrupted. Please fix it before using the replier module.")
                return None
    else:
        return []


# Print the number of times a message has been triggered
async def count(client, logger, message, action, args, author):
    replies = await load_replies(client, message)
    if (replies is None):
        return
    if (args is None or len(args) == 0):
        await client.send_message(message.channel, "Try with an argument for this command next time.")
        return
    else:
        for arg in args:
            reply = get_reply(replies, arg)
            if (reply is None):
                await client.send_message(message.channel, "The trigger %s doesn't even exist." % arg)
            else:
                await client.send_message(message.channel, "The trigger %s has been called %d times." % (arg, reply["count"]))


# Manage the printing and setting of triggered messages
async def main(client, logger, message, action, args, author):
    replies = await load_replies(client, message)
    if (replies is None):
        return
    # Call the triggered message
    if (args is None or len(args) == 0):
        reply = get_reply(replies, action)
        if (reply is not None):
            await client.send_message(message.channel, reply["message"])
            reply["count"] += 1
            with open(REPLIES_FILE, 'w') as replies_file:
                hjson.dump(replies, replies_file, indent=' ' * 2)
        else:
            await client.send_message(message.channel, "I know nothing about this. I swear!")

    # Assign a message to this trigger
    elif (args[0] == "="):
        if (len(args) > 1):
            # Check if the reply dict already exist
            old_dict = get_reply(replies, action)
            # If the reply dict exist, replace it
            if (old_dict is None):
                new_dict = OrderedDict(trigger=action,
                                       message=" ".join(args[1:]),
                                       count=0)
                replies.append(new_dict)
            else:
                if (not await opmod.isop_user(message.author) and old_dict["locked"] is True):
                    await client.send_message(message.channel, "Sorry, the %s trigger has been locked by an operator." % action)
                    return
                else:
                    old_dict["trigger"] = action
                    old_dict["message"] = " ".join(args[1:])
                    old_dict["count"] = 0
                    old_dict["locked"] = False
            await client.send_message(message.channel, "Roger that, %s trigger has been registered." % action)
            with open(REPLIES_FILE, 'w') as replies_file:
                hjson.dump(replies, replies_file, indent=' ' * 2)
        else:
            await client.send_message(message.channel, "You should try to put a message to assign to this trigger.")
            return
    return
