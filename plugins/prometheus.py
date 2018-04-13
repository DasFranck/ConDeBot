#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from classes.Plugin import Plugin
from prometheus_client import start_http_server, Counter

NAME = "Prometheus"
DESCRIPTION = None
USAGE = {}


class PrometheusPlugin(Plugin):
    def __init__(self, cdb):
        super().__init__(cdb)

        cdb.reserve_keywords(["prometheus"], NAME)
        cdb.add_plugin_description(DESCRIPTION, NAME)
        cdb.add_plugin_usage(USAGE, NAME)

        start_http_server(9100)
        # Maybe too much labals, can overload Prometheus: https://prometheus.io/docs/practices/instrumentation/#do-not-overuse-labels
        self.reserved_keywords_calls = Counter("reserved_keywords_calls", "Reserved Keywords Calls", ["keyword", "author_id", "server_id", "channel_id"])

    async def on_message(self, message, cmd):
        if cmd.triggered and cmd.action in self.cdb._reserved_keywords:
            self.reserved_keywords_calls.labels(cmd.action, cmd.author.id, cmd.channel.server.id, cmd.channel.id).inc()

        if not cmd.triggered \
           or cmd.action not in ["prometheus"]:
            return
