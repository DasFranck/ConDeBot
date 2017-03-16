#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
import hjson
import os
import random

from config import LISTS_FILE_DIR
from classes.Plugin import Plugin
from utilities import get_meta, isop_user


# Load the lists file into an array of dict
def load_lists(lists_path):
    if (os.path.isfile(lists_path)):
        with open(lists_path) as lists_file:
            try:
                return hjson.load(lists_file)
            except:
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


# Write the lists to the hjson file
def write_to_file(lists_path, lists):
    with open(lists_path, 'w') as lists_file:
        hjson.dump(lists, lists_file, indent=' ' * 2)


class ListPlugin(Plugin):
    def __init__(self, cdb):
        super().__init__(cdb)
        if not os.path.isdir(LISTS_FILE_DIR):
            os.makedirs(LISTS_FILE_DIR)

    async def add_to_list(self, lists, list_name, content, message, author):
        old_dict = get_list(lists, list_name)
        if (old_dict is None):
            new_dict = OrderedDict(name=list_name, list=[content], count=0, locked=False)
            lists.append(new_dict)
            self.cdb.logger.log_info_command("The new list %s has been created by %s" % (list_name, author), message)
        else:
            # Check if the reply dict is locked
            if (not isop_user(message.author) and "locked" in old_dict and old_dict["locked"] is True):
                await self.cdb.send_message(message.channel, "Sorry, the %s list has been locked by an operator." % list_name)
                self.cdb.logger.log_warn_command("The locked list %s modification has been requested by NON-OP %s, FAILED" % (list_name, author), message)
                return lists
            else:
                old_dict["list"].append(content)
                self.cdb.logger.log_info_command("A new element has been added in the list %s by %s" % (list_name, author), message)
        await self.cdb.send_message(message.channel, "Roger that, a new element has been added in %s (index: %d)." % (list_name, len(get_list(lists, list_name)["list"]) - 1))
        return lists

    async def write_random_from_list(self, lists, list_name, message, author):
        list = get_list(lists, list_name)
        index = random.randrange(len(list["list"]))
        await self.cdb.send_message(message.channel, list["list"][index])
        await self.cdb.send_message(message.channel, str(index))
        self.cdb.logger.log_info_command("A random content from the list %s has been requested by %s" % (list_name, author), message)
        list["count"] += 1
        return lists

    async def on_message(self, message):
        (msg, args, author, triggered, action) = get_meta(self.cdb, message)
        if not triggered or action != "list":
            return

        # Set file path
        if message.server is not None:
            lists_path = LISTS_FILE_DIR + message.server.id + ".json"
        else:
            lists_path = LISTS_FILE_DIR + "dump.json"

        # Load JSON lists file
        lists = load_lists(lists_path)
        if (lists is None):
            self.cdb.logger.error("JSON lists file loading failed.")
            await self.cdb.send_message(message.channel, "The JSON lists file seems corrupted. Please fix it before using the replier module.")
            return

        if len(args) > 1:
            if args[1] == "add":
                if len(args) == 2:
                    await self.cdb.send_message(message.channel, "Try with a content to put in the list next time.")
                else:
                    new_lists = await self.add_to_list(lists, args[0], " ".join(args[2:]), message, author)
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
            new_lists = await self.write_random_from_list(lists, args[0], message, author)
            write_to_file(lists_path, new_lists)

        else:
            await self.cdb.send_message(message.channel, "Try with an argument for this command next time.")
            return
        return