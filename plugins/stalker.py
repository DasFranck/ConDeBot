#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from classes.Plugin import Plugin
from utilities import isop_user, get_meta, display_error


class StalkerPlugin(Plugin):
    async def on_message(self, message):
        (msg, args, author, triggered, action) = get_meta(self.cdb, message)
        if (triggered and action in ["stalk"]):
            if not isop_user(message.author):
                await display_error(self.cdb, message.channel, "You don't have the right to do that.")
                self.cdb.logger.log_warn_command("Stalker command use requested by NON-OP %s, FAILED" % (author), message)

    async def on_member_update(self, before, after):
        if (before.status != after.status):
            print("{}: {} ({}) status has changed from {} to {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), after.name, after.id, before.status, after.status))
        if (before.game != after.game):
            print("{}: {} ({}) game has changed from {} to {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), after.name, after.id, str(before.game), str(after.game)))
        if (before.avatar != after.avatar):
            print("{}: {} ({}) avatar has changed".format(time.strftime("%Y-%m-%d %H:%M:%S"), after.name, after.id))
            pass
        if (before.nick != after.nick):
            pass
        #if (before.role != after.role):
        #    pass
        pass