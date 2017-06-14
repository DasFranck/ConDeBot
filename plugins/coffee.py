#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import json

from classes.Plugin import Plugin


class CoffeePlugin(Plugin):
    async def on_message(self, message, cmd):
        if not cmd \
           or not cmd.triggered:
            return

        # Serve a delicious coffee (Module: "coffee")
        if cmd.action in ["café", "cafe", "coffee"]:
            self.cdb.logger.log_info_command("Coffee requested by " + cmd.author_nickdis,
                                             message)
            await self.cdb.send_message(message.channel, ":coffee:")
            await self.cdb.send_message(message.channel,
                                        self.serve(message, cmd.args, "coffee"))
        # Serve a delicious tea (Module: "coffee")
        elif cmd.action in ["thé", "the", "tea"]:
            self.cdb.logger.log_info_command("Tea requested by " + cmd.author_nickdis,
                                             message)
            await self.cdb.send_message(message.channel, ":tea:")
            await self.cdb.send_message(message.channel,
                                        self.serve(message, cmd.args, "tea"))

    def serve(self, message, args, drink):
        """
        Check if the coffee is for someone else
        (And if the sender didn't forget the recipient)
        """
        with open("jsonfiles/coffee.json", 'r') as quotes_file:
            quotes = json.load(quotes_file)
            if ('>' in args):
                index = args.index('>') + 1
                return ("Here {}, that's your {}.\n{}".format(
                    " ".join(args[index:]),
                    drink,
                    random.choice(quotes[drink]))
                )
            else:
                return ("Here {}, that's your {}.\n{}".format(
                    message.author.mention,
                    drink,
                    random.choice(quotes[drink]))
                )
