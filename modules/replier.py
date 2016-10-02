#!/usr/bin/env python3
# -*- coding: utf-8 -*-

REPLIES_FILE_PATH = "jsonfiles/"
REPLIES_FILE = REPLIES_FILE_PATH + "replies.json"

try:
    import os
    import json
except ImportError as message:
    print("Missing package(s) for the replier module: %s" % message)
    exit(12)

# return False if the command asked doesn't exist, return True otherwise or when setting
async def main(client, logger, message, action, args, nick):
    #if (os.path.isfile(REPLIES_FILE)):
    #    with open(REPLIES_FILE) as replies_file:
    #        replies = json.load(replies_file)
    #else:
    #    return False
    if (args is None or len(args) == 0):

    elif (args[1] == "="):

    else:

    return False
