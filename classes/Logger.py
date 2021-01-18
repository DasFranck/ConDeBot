#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
import logging
import os


class Logger(logging.Logger):
    def __init__(self):
        super().__init__("discord")
        # Set logger level to INFO
        self.setLevel(logging.INFO)

        os.makedirs("logs", exist_ok=True)

        # Setting handler (Log File)
        handler = logging.FileHandler(filename='logs/discord.log',
                                      encoding='utf-8',
                                      mode='a')
        handler.setFormatter(logging.Formatter(
            "%(asctime)s :: %(levelname)s :: %(message)s"))
        self.addHandler(handler)

        # Setting stream_handler (Stdout)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        self.addHandler(stream_handler)

        self.info("#-------------START-------------#")

    def log_info(self, string, message):
        """ Add an entry in the log with info level. """
        if isinstance(message.channel, discord.abc.PrivateChannel):
            self.info("%s in a Private Channel", string)
        else:
            self.info("{} in #{} on {} ({})".format(string,
                                                    message.channel.name,
                                                    message.guild.name,
                                                    message.guild.id))

    def log_error(self, string, message):
        """ Add an entry in the log with error level. """
        if isinstance(message.channel, discord.abc.PrivateChannel):
            self.error("%s in a Private Channel", string)
        else:
            self.error("{} in #{} on {} ({})".format(string,
                                                     message.channel.name,
                                                     message.guild.name,
                                                     message.guild.id))

    def log_warn(self, string, message):
        """ Add an entry in the log with warn level. """
        if isinstance(message.channel, discord.abc.PrivateChannel):
            self.warning("%s in a Private Channel", string)
        else:
            self.warning("{} in #{} on {} ({})".format(string,
                                                       message.channel.name,
                                                       message.guild.name,
                                                       message.guild.id))
