#!/usr/bin/env python3
# -*- coding: utf-8 -*-

NAME = "ConDeBot"

try:
    import discord
    from plugins import opmod
except ImportError as message:
    print("Missing package(s) for %s: %s" % (NAME, message))
    exit(12)

#
status_dict = {"online": discord.Status.online,
               "offline": discord.Status.offline,
               "idle": discord.Status.idle,
               "dnd": discord.Status.do_not_disturb,
               "do_not_disturb": discord.Status.do_not_disturb,
               "invisible": discord.Status.invisible}


# Thanks to SO, a static variable decorator
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


@static_vars(game=None, status=None)
async def main(client, logger, message, action, args, author):
    if not await opmod.isop_user(message.author):
        await client.send_message(message.channel, "You don't have the right to do that.")
        logger.log_warn_command("Changing bot status requested by NON-OP %s, FAILED" % (author), message)
    else:
        if action == "status":
            if len(args) == 0:
                await client.send_message(message.channel, "Try with an argument for this command next time.")
                await client.send_message(message.channel, "Valid arguments: online, offline, idle, dnd, invisible.")
            elif args[0].lower() in status_dict:
                logger.log_info_command("Change bot's status to %s requested by %s" % (args[0].lower(), author), message)
                main.status = status_dict[args[0].lower()]
            else:
                await client.send_message(message.channel, "It's not a valid argument.")
                await client.send_message(message.channel, "Valid arguments: online, offline, idle, dnd, invisible.")
        elif action == "game":
            if len(args) == 0:
                main.game = None
                logger.log_info_command("Erasing bot's game requested by %s" % (author), message)
            else:
                main.game = discord.Game(name=message.content[6:])
                logger.log_info_command("Change bot's game requested by %s" % (author), message)
        await client.change_presence(game=main.game, status=main.status)
