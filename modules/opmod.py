#!/usr/bin/env python3
# -*- coding: utf-8 -*-

NAME = "ConDeBot"
OPS_FILE_PATH = "jsonfiles/"
OPS_FILE = OPS_FILE_PATH + "ops.json"


try:
    import json
    import os
    import discord
    from modules.utilities import get_nickdis
except ImportError as message:
    print('Missing package(s) for %s: %s' % (NAME, message))
    exit(12)


# Check if user is op (NOT LOGGED FUNCTION, meant to be use in the source code of CDB)
async def isop_user(user):
    nickdis = ""
    if (isinstance(user, str)):
        nickdis = user
    elif (isinstance(user, discord.User)):
        nickdis = get_nickdis(user)
    else:
        return (False)

    if (os.path.isfile(OPS_FILE)):
        with open(OPS_FILE) as ops_file:
            ops = json.load(ops_file)
        return (nickdis in ops)
    else:
        return (False)


# Check if user is op (LOGGED FUNCTION, meant to be used via !isop "nickdis")
async def isop_l(client, logger, message, author, arg):
    logger.log_info_command("Operator status of %s (%s) requested by %s" % (arg, await isop_user(arg), author), message)
    if (await isop_user(arg)):
        await client.send_message(message.channel, "%s is an operator" % arg)
    else:
        await client.send_message(message.channel, "%s is not an operator" % arg)
    return


# Check if user who called the command is op (LOGGED FUNCTION, meant to be used via !isop)
async def isop_s(client, logger, message, author):
    logger.log_info_command("Operator status of %s (%s) requested by %s" % (message.author, await isop_user(message.author), author), message)
    if (await isop_user(message.author)):
        await client.send_message(message.channel, "You are an operator")
    else:
        await client.send_message(message.channel, "You are not an operator")
    return


# Op user
async def op_him(client, logger, message, author, arg, ops):
    if (not await isop_user(message.user)):
        await client.send_message(message.channel, "You don't have the right to do that.")
        logger.log_warn_command("Adding operator (%s) requested by NON-OP %s, FAILED" % (arg, author), message)
        return (ops)

    if (await isop_user(arg)):
        await client.send_message(message.channel, "%s is already an operator" % arg)
        logger.log_info_command("Adding operator (%s) requested by %s, failed cause he's already an operator" % (arg, author), message)
        return (ops)

    ops.append(arg)
    with open(OPS_FILE, 'w') as ops_file:
        json.dump(ops, ops_file)
    await client.send_message(message.channel, "%s has been added as operator" % arg)
    logger.log_info_command("Adding operator (%s) requested by %s, OK" % (arg, author), message)
    return (ops)


# Deop user
async def deop_him(client, logger, message, author, arg, ops):
    if (not isop_user(message.user)):
        await client.message(message.channel, "You don't have the right to do that.")
        logger.log_warn_command("Deleting operator (%s) requested by NON-OP %s, FAILED" % (arg, author), message)
        return (ops)

    if (not isop_user(arg)):
        await client.message(message.channel, "%s is already not an operator" % arg)
        logger.log_info_command("Deleting operator (%s) requested by %s, failed cause he's not an operator" % (arg, author), message)
        return (ops)

    with open(OPS_FILE, 'w') as ops_file:
        json.dump(ops, ops_file)
    ops.remove(arg)
    await client.send_message(message.channel, "%s has been removed from operator list" % arg)
    logger.log_info_command("Deleting operator (%s) requested by %s, OK" % (arg, author), message)
    return (ops)


# Op user
async def op_list(client, message, ops, logger, author):
    string = "Operator list:\n"
    for op in ops:
        if (op is ops[-1]):
            string += "%s" % op
        else:
            string += "%s, " % op
    await client.send_message(message.channel, string)
    logger.log_info_command("Operator list requested by %s" % author, message)
    return


# The main manager
async def main(client, logger, message, action, args, author):
    if (not os.path.exists(OPS_FILE_PATH)):
        os.makedirs(OPS_FILE_PATH)

    ops = []
    # If json file exist, load it
    if (os.path.isfile(OPS_FILE)):
        with open(OPS_FILE) as ops_file:
            ops = json.load(ops_file)

    if (action == "op"):
        for arg in args:
            ops = await op_him(client, logger, message, author, arg, ops)
    elif (action == "deop"):
        for arg in args:
            ops = await deop_him(client, logger, message, author, arg, ops)
    elif (action == "isop"):
        if (len(args) == 0):
            await isop_s(client, logger, message, author)
        else:
            for arg in args:
                await isop_l(client, logger, message, author, arg)
    elif (action == "op_list"):
        await op_list(client, message, ops, logger, author)

    with open(OPS_FILE, 'w') as ops_file:
        json.dump(ops, ops_file)
    return
