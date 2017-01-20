#!/usr/bin/env python3
# -*- coding: utf-8 -*-

NAME = "ConDeBot"

try:
    import codecs
    import random
except ImportError as message:
    print('Missing package(s) for %s: %s' % (NAME, message))
    exit(12)


# Display random quotes of Kaamelott
async def quote(client, logger, message, author):
    fd_kaam = codecs.open("txtfiles/kaamelott.txt", "r", "utf-8")
    buf = fd_kaam.read()
    nb = random.randint(1, int(buf[0:buf.index('\n')]))
    beg_quote = buf.find("#" + str(nb))
    end_quote = beg_quote + buf[beg_quote:].find("\n\n") + 1

    logger.log_info_command("Random Kaamelott Quote (#" + str(nb) + ") was requested by " + author, message)
    await client.send_message(message.channel, buf[beg_quote:end_quote])
    fd_kaam.close()
    return


# Display specific quotes of Kaamelott
async def spec(client, logger, message, args, author):
    fd_kaam = codecs.open("txtfiles/kaamelott.txt", "r", "utf-8")
    buf = fd_kaam.read()

    if (len(args) == 1):
        logger.log_info_command("Number of Kaamelott Quote (" + buf[0:buf.index('\n')] + ") was requested by " + author, message)
        await client.send_message(message.channel, "There's " + buf[0:buf.index('\n')] + " Kaamelott Quote")
        fd_kaam.close()
        return

    nb = int(args[1])
    if (nb > int(buf[0:buf.index('\n')])):
        logger.log_warn_command("Non-existant Kaamelott Quote #" + str(nb) + " was requested by " + author, message)
        await client.send_message(message.channel, "FAILED : Kaamelott Quote #" + str(nb) + " doesn't exist")
        fd_kaam.close()
        return

    beg_quote = buf.find("#" + str(nb))
    end_quote = beg_quote + buf[beg_quote:].find("\n\n") + 1
    logger.log_info_command("Kaamelott Quote #" + str(nb) + " was requested by " + author, message)
    await client.send_message(message.channel, buf[beg_quote:end_quote])
    fd_kaam.close()
    return


# Manage Kaamelott
async def main(client, logger, message, args, author):
    if (len(args) == 0):
        await quote(client, logger, message, author)
    elif (len(args) >= 1 and args[0] == "-q"):
        await spec(client, logger, message, args, author)
    return
