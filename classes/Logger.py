#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        return

    def log_info_command(self, string, message):
        """ Add an entry in the log with info level. """
        if (message.channel.is_private is True):
            self.info(string + " in a Private Channel")
        else:
            self.info("{} in #{} on {} (%{})".format(string,
                                                     message.channel.name,
                                                     message.server.name,
                                                     message.server.id))

    def log_error_command(self, string, message):
        """ Add an entry in the log with error level. """
        if (message.channel.is_private is True):
            self.error(string + " in a Private Channel")
        else:
            self.error("{} in #{} on {} (%{})".format(string,
                                                      message.channel.name,
                                                      message.server.name,
                                                      message.server.id))

    def log_warn_command(self, string, message):
        """ Add an entry in the log with warn level. """
        if (message.channel.is_private is True):
            self.warn(string + " in a Private Channel")
        else:
            self.warn("{} in #{} on {} (%{})".format(string,
                                                     message.channel.name,
                                                     message.server.name,
                                                     message.server.id))
