#!/usr/bin/env python3
# -*- coding: utf-8 -*-

NAME = "ConDeBot"

try:
    from modules import opmod
except ImportError as message:
    print("Missing package(s) for %s: %s" % (NAME, message))
    exit(12)


async def main(client, logger, message, action, author):
    if (not await opmod.isop_user(message.author)):
        await client.send_message(message.channel, "You don't have the right to do that.")
        logger.log_warn_command("Bot Suicide requested by NON-OP %s, FAILED" % (author), message)
    else:
        if (action == "slain"):
            await client.send_message(message.channel, "%s has been slained by %s." % (NAME, author))
        elif (action == "kill"):
            await client.send_message(message.channel, "%s has been killed by %s." % (NAME, author))
        elif (action == "suicide"):
            await client.send_message(message.channel, "%s is suiciding himself. With %s's help." % (NAME, author))
        logger.log_info_command("Bot has been terminated by " + author, message)
        logger.logger.info("#--------------END--------------#")

        # Trying to exit properly (client.py:494 from discord.py)
        await client.logout()
