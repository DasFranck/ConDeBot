#!/usr/bin/env python3
# -*- coding: utf-8 -*-

NAME = "ConDeBot"

try:
    import asyncio
    import sys
except ImportError as message:
    print("Missing package(s) for %s: %s" % (NAME, message))
    exit(12)


def kill_me(client):
    pending = asyncio.Task.all_tasks()
    gathered = asyncio.gather(*pending)
    try:
        gathered.cancel()
        client.loop.run_until_complete(gathered)
        gathered.exception()
    except:
        pass
    client.loop.stop()
    return


async def main(client, logger, message, action, nick):
    if (action == "slain"):
        await client.send_message(message.channel, "%s has been slained by %s." % (NAME, nick))
    elif (action == "kill"):
        await client.send_message(message.channel, "%s has been killed by %s." % (NAME, nick))
    elif (action == "suicide"):
        await client.send_message(message.channel, "%s is suiciding himself. With %s's help." % (NAME, nick))
    logger.log_info_command("Bot has been terminated by " + nick, message)
    logger.logger.info("#--------------END--------------#")

    # Trying to exit properly (client.py:494 from discord.py)
    await client.logout()
