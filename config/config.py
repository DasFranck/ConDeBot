#!/usr/bin/env python3
# -*- coding: utf-8 -*-

NAME = "ConDeBot"
SHORT_NAME = "CDB"
DESCRIPTION = "ConDeBot - Un con de bot Discord"
CMD_PREFIX = ""

# Those path concatenations looks a bit insecure
DATA_PATH = "./data/"
OPS_FILE_PATH = DATA_PATH + "jsonfiles/"
OPS_FILE = DATA_PATH + OPS_FILE_PATH + "ops.json"
REPLIES_FILE_DIR = DATA_PATH + "jsonfiles/replies/"
LISTS_FILE_DIR = DATA_PATH + "jsonfiles/lists/"

token = ""

# Plugin configuration
# The variables must begin by the uppercase name of the plugin

STALKER_AUTOSTART = False
