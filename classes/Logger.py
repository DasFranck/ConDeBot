#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os


class Logger:
    logger = logging.getLogger('discord')

    def __init__(self):
        # Set logger level to INFO
        self.logger.setLevel(logging.INFO)

        if not (os.path.exists("logs")):
            os.makedirs("logs")

        # Setting handler (Log File)
        handler = logging.FileHandler(filename='logs/discord.log',
                                      encoding='utf-8',
                                      mode='a')
        handler.setFormatter(logging.Formatter(
            "%(asctime)s :: %(levelname)s :: %(message)s"))
        self.logger.addHandler(handler)

        # Setting stream_handler (Stdout)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        self.logger.addHandler(stream_handler)

        self.logger.info("#-------------START-------------#")
        return

    def log_info_command(self, string, message):
        """ Add an entry in the log with info level. """
        if (message.channel.is_private is True):
            self.logger.info(string + " in a Private Channel")
        else:
            self.logger.info("{} in #{} on {} (%{})".format(string,
                                                            message.channel.name,
                                                            message.server.name,
                                                            message.server.id))

    def log_error_command(self, string, message):
        """ Add an entry in the log with error level. """
        if (message.channel.is_private is True):
            self.logger.error(string + " in a Private Channel")
        else:
            self.logger.error("{} in #{} on {} (%{})".format(string,
                                                             message.channel.name,
                                                             message.server.name,
                                                             message.server.id))

    def log_warn_command(self, string, message):
        """ Add an entry in the log with warn level. """
        if (message.channel.is_private is True):
            self.logger.warn(string + " in a Private Channel")
        else:
            self.logger.warn("{} in #{} on {} (%{})".format(string,
                                                            message.channel.name,
                                                            message.server.name,
                                                            message.server.id))
