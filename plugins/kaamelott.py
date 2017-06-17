#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import random

from classes.Plugin import Plugin


class KaamelottPlugin(Plugin):
    async def on_message(self, message, cmd):
        if not cmd \
           or not cmd.triggered \
           or not cmd.action == "kaamelott":
            return

        if (len(cmd.args) == 0):
            await self.quote(message, cmd.author_nickdis)
        elif (len(cmd.args) >= 1 and cmd.args[0] == "-q"):
            await self.spec(message, cmd.args, cmd.author_nickdis)
        return

    # Display random quotes of Kaamelott
    async def quote(self, message, author):
        fd_kaam = codecs.open("data/txtfiles/kaamelott.txt", "r", "utf-8")
        buf = fd_kaam.read()
        nb = random.randint(1, int(buf[0:buf.index('\n')]))
        beg_quote = buf.find("#" + str(nb))
        end_quote = beg_quote + buf[beg_quote:].find("\n\n") + 1

        self.cdb.log_info_command("Random Kaamelott Quote (#" + str(nb) + ") was requested by " + author, message)
        await self.cdb.send_message(message.channel, buf[beg_quote:end_quote])
        fd_kaam.close()
        return

    # Display specific quotes of Kaamelott
    async def spec(self, message, args, author):
        fd_kaam = codecs.open("data/txtfiles/kaamelott.txt", "r", "utf-8")
        buf = fd_kaam.read()

        if (len(args) == 1):
            self.cdb.log_info_command("Number of Kaamelott Quote (" + buf[0:buf.index('\n')] + ") was requested by " + author, message)
            await self.cdb.send_message(message.channel, "There's " + buf[0:buf.index('\n')] + " Kaamelott Quote")
            fd_kaam.close()
            return

        nb = int(args[1])
        if (nb > int(buf[0:buf.index('\n')])):
            self.cdb.log_warn_command("Non-existant Kaamelott Quote #" + str(nb) + " was requested by " + author, message)
            await self.cdb.send_message(message.channel, "FAILED : Kaamelott Quote #" + str(nb) + " doesn't exist")
            fd_kaam.close()
            return

        beg_quote = buf.find("#" + str(nb))
        end_quote = beg_quote + buf[beg_quote:].find("\n\n") + 1
        self.cdb.log_info_command("Kaamelott Quote #" + str(nb) + " was requested by " + author, message)
        await self.cdb.send_message(message.channel, buf[beg_quote:end_quote])
        fd_kaam.close()
        return
