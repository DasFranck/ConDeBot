#!/usr/bin/env python3
# -*- coding: utf-8 -*-

NAME = "ConDeBot"
OPS_FILE_PATH = "jsonfiles/"
OPS_FILE = OPS_FILE_PATH + "ops.json"


try:
    import json
    import os
except ImportError as message:
    print('Missing package(s) for %s: %s' % (NAME, message))
    exit(12)


# Check if user is op (NOT LOGGED FUNCTION, meant to be use in the source code of CDB)
async def isop_user(user):
    if (os.path.isfile(OPS_FILE)):
        with open(OPS_FILE) as ops_file:
            ops = json.load(ops_file)
        return ((user.name + "#" + str(user.disciminator)) in ops)
    else:
        return (False)

async def isop_nickdis(nickdis):
    if (os.path.isfile(OPS_FILE)):
        with open(OPS_FILE) as ops_file:
            ops = json.load(ops_file)
        return (nickdis in ops)
    else:
        return (False)

# Check if user is op (LOGGED FUNCTION, meant to be used via !cdb isop)
async def isop_l(client, logger, message, nickdis, nick):
    logger.log_info_command("Operator status of %s (%s) requested by %s" % (nickdis, await isop_nickdis(nickdis), nick), message)
    if (await isop_nickdis(nickdis)):
        await client.send_message(message.channel, "%s is an operator" % nickdis)
    else:
        await client.send_message(message.channel, "%s is not an operator" % nickdis)
    return


# Op user
async def op_him(client, logger, message, nickdis, nick, ops):
    if (not await isop_user(message.user)):
        await client.send_message(message.channel, "You don't have the right to do that.")
        logger.log_warn_command("Adding operator (%s) requested by NON-OP %s, FAILED" % (nickdis, nick), message)
        return (ops)

    if (await isop_nickdis(nickdis)):
        await client.send_message(message.channel, "%s is already an operator" % nickdis)
        logger.log_info_command("Adding operator (%s) requested by %s, failed cause he's already an operator" % (nickdis, nick), message)
        return (ops)

    ops.append(nickdis)
    with open(OPS_FILE, 'w') as ops_file:
        json.dump(ops, ops_file)
    await client.send_message(message.channel, "%s has been added as operator" % nickdis)
    logger.log_info_command("Adding operator (%s) requested by %s, OK" % (nickdis, nick), message)
    return (ops)


# Deop user
async def deop_him(client, logger, message, nickdis, nick, ops):
    if (not isop_user(message.user)):
        await client.message(message.channel, "You don't have the right to do that.")
        logger.log_warn_command("Deleting operator (%s) requested by NON-OP %s, FAILED" % (nickdis, nick), message)
        return (ops)

    if (not isop_nickdis(nickdis)):
        await client.message(message.channel, "%s is already not an operator" % nickdis)
        logger.log_info_command("Deleting operator (%s) requested by %s, failed cause he's not an operator" % (nickdis, nick), message)
        return (ops)

    with open(OPS_FILE, 'w') as ops_file:
        json.dump(ops, ops_file)
    ops.remove(nickdis)
    await client.send_message(message.channel, "%s has been removed from operator list" % nickdis)
    logger.log_info_command("Deleting operator (%s) requested by %s, OK" % (nickdis, nick), message)
    return (ops)


# Op user
async def op_list(client, message, ops, logger, nick):
    string = "Operator list:\n"
    for op in ops:
        if (op == ops[-1]):
            string += "%s" % op
        else:
            string += "%s, " % op
    await client.send_message(message.channel, string)
    logger.log_info_command("Operator list requested by %s" % nick, message)
    return


# The main manager
async def main(client, logger, message, action, args, nick):
    if (not os.path.exists(OPS_FILE_PATH)):
        os.makedirs(OPS_FILE_PATH)

    ops = []
    # If json file exist, load it
    if (os.path.isfile(OPS_FILE)):
        with open(OPS_FILE) as ops_file:
            ops = json.load(ops_file)

    if (action == "op"):
        for nickdis in args:
            ops = await op_him(client, logger, message, nickdis, nick, ops)
    elif (action == "deop"):
        for nickdis in args:
            ops = await deop_him(client, logger, message, nickdis, nick, ops)
    elif (action == "isop"):
        for nickdis in args:
            await isop_l(client, logger, message, nickdis, nick)
    elif (action == "list_op"):
        await op_list(client, message, ops, logger, nick)

    with open(OPS_FILE, 'w') as ops_file:
        json.dump(ops, ops_file)
    return
