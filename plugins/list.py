#!/usr/bin/env python3
# -*- coding: utf-8 -*-

LISTS_FILE_DIR = "jsonfiles/lists/"

from collections import OrderedDict
from plugins import opmod
import hjson
import os
import random


# Load the lists file into an array of dict
async def load_lists(client, message, logger, lists_path):
    if (os.path.isfile(lists_path)):
        with open(lists_path) as lists_file:
            try:
                return hjson.load(lists_file)
            except:
                logger.logger.error("JSON lists file loading failed.")
                await client.send_message(message.channel, "The JSON lists file seems corrupted. Please fix it before using the replier module.")
                return None
    else:
        return []


# Get the reply dict assign to the trigger
def get_list(lists, name):
    if (lists is None):
        return None
    for list in lists:
        if (list["name"] == name):
            return list
    return None


async def add_to_list(client, logger, lists, list_name, content, message, author):
    old_dict = get_list(lists, list_name)
    if (old_dict is None):
        new_dict = OrderedDict(name=list_name, list=[content], count=0, locked=False)
        lists.append(new_dict)
        logger.log_info_command("The new list %s has been created by %s" % (list_name, author), message)
    else:
        # Check if the reply dict is locked
        if (not await opmod.isop_user(message.author) and "locked" in old_dict and old_dict["locked"] is True):
            await client.send_message(message.channel, "Sorry, the %s list has been locked by an operator." % list_name)
            logger.log_warn_command("The locked list %s modification has been requested by NON-OP %s, FAILED" % (list_name, author), message)
            return lists
        else:
            old_dict["list"].append(content)
            logger.log_info_command("A new element has been added in the list %s by %s" % (list_name, author), message)
    await client.send_message(message.channel, "Roger that, a new element has been added in %s (index: %d)." % (list_name, len(get_list(lists, list_name)["list"]) - 1))
    return lists


async def write_random_from_list(logger, lists, list_name, client, message):
    list = get_list(lists, list_name)
    index = random.randrange(len(list["list"]))
    await client.send_message(message.channel, list["list"][index])
    await client.send_message(message.channel, str(index))
    logger.log_info_command("A random content from the list %s has been requested by %s" % (list_name, author), message)
    list["count"] += 1
    return lists


def write_to_file(lists_path, lists):
    with open(lists_path, 'w') as lists_file:
        hjson.dump(lists, lists_file, indent=' ' * 2)


async def main(client, logger, message, action, args, author):
    if not os.path.isdir(LISTS_FILE_DIR):
        os.makedirs(LISTS_FILE_DIR)

    # Set file path
    if message.server is not None:
        lists_path = LISTS_FILE_DIR + message.server.id + ".json"
    else:
        lists_path = LISTS_FILE_DIR + "dump.json"

    # Load JSON lists file
    lists = await load_lists(client, message, logger, lists_path)
    if (lists is None):
        return

    if len(args) > 1:
        if args[1] == "add":
            if len(args) == 2:
                await client.send_message(message.channel, "Try with a content to put in the list next time.")
            else:
                new_lists = await add_to_list(client, logger, lists, args[0], " ".join(args[2:]), message, author)
                write_to_file(lists_path, new_lists)
        if args[1] == "get":
            pass
        if args[1] == "del":
            pass
        if args[1] == "count":
            pass
        if args[1] == "size":
            pass
        if args[1] == "lock":
            pass

    elif len(args) == 1:
        new_lists = await write_random_from_list(logger, lists, args[0], client, message)
        write_to_file(lists_path, new_lists)

    else:
        await client.send_message(message.channel, "Try with an argument for this command next time.")
        return
    return
