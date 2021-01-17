#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import hjson

from classes.Plugin import Plugin

NAME = "Coffee"
DESCRIPTION = "Serve some coffee"
USAGE = {
    "_": ("!coffee: Serve a delicious coffee\n"
          "!tea: Serve a delicious tea"
          )
}


class CoffeePlugin(Plugin):
    def __init__(self, cdb):
        super().__init__(cdb)

        cdb.add_plugin_description(DESCRIPTION, NAME)
        cdb.add_plugin_usage(USAGE, NAME)
        cdb.reserve_keywords(["café", "cafe", "coffee", "thé", "the", "tea"], NAME)

        self.COFFEE_FILE_PATH = self.cdb.CDB_PATH + "plugins/coffee/quotes.json"

    async def on_message(self, message, cmd):
        if not cmd or not cmd.triggered:
            return

        # Serve a delicious coffee (Module: "coffee")
        if cmd.action in ["café", "cafe", "coffee"]:
            self.cdb.log_info("Coffee requested by %s" % str(cmd.author), message)
            await message.channel.send(":coffee:")
            await message.channel.send(self.serve(message, cmd.args, "coffee"))

        # Serve a delicious tea (Module: "coffee")
        elif cmd.action in ["thé", "the", "tea"]:
            self.cdb.log_info("Tea requested by %s" % str(cmd.author), message)
            await message.channel.send(":tea:")
            await message.channel.send(self.serve(message, cmd.args, "tea"))

    def serve(self, message, args, drink):
        """
        Check if the coffee is for someone else
        (And if the sender didn't forget the recipient)
        """
        with open(self.COFFEE_FILE_PATH, 'r', encoding="utf8") as quotes_file:
            quotes = hjson.load(quotes_file)
            if ('>' in args):
                index = args.index('>') + 1
                return f"Here {' '.join(args[index:])}, that's your {drink}.\n{random.choice(quotes[drink])}"
            else:
                return f"Here {message.author.mention}, that's your {drink}.\n{random.choice(quotes[drink])}"
