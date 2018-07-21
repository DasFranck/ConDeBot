#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dice import roll, DiceBaseException
from dice.elements import Roll, Integer

from classes.Plugin import Plugin

NAME = "Roll"
DESCRIPTION = "Roll the dices"
USAGE = {
    "_": ("!roll: Roll the dices!\n"
          "More information about the syntax here: "
          "https://github.com/borntyping/python-dice#notation"
          )
}


class RollPlugin(Plugin):
    def __init__(self, cdb):
        super().__init__(cdb)

        cdb.add_plugin_description(DESCRIPTION, NAME)
        cdb.add_plugin_usage(USAGE, NAME)
        cdb.reserve_keywords(["roll"], NAME)

    async def on_message(self, message, cmd):
        if (not cmd or not cmd.triggered
            or cmd.action not in ["roll"]):
            return

        if len(cmd.args) == 0:
            await self.cdb.send_message(cmd.msg.channel,
                                        "Try with an argument for this command next time.")
            return

        try:
            result = roll(" ".join(cmd.args))
        except DiceBaseException as e:
            await self.cdb.send_message(cmd.msg.channel,
                                        "Error: \n```" + e.pretty_print() + "```")
            return

        if type(result) is Integer:
            await self.cdb.send_message(cmd.msg.channel,
                                        "The result is: " + str(result))
        elif type(result) in [Roll, list]:
            await self.cdb.send_message(cmd.msg.channel,
                                        "The dices are: " + ", ".join(str(dice) for dice in result[:]))
        else:
            await self.cdb.send_message(cmd.msg.channel,
                                        "That seems to be an unexpected result, please contact DasFranck.")
            print(result)
            print(type(result))
        return