#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from classes.Plugin import Plugin
import importlib
import inspect
import os


class PluginManager:
    def __init__(self, cdb):
        self.cdb = cdb
        self.cdb.plugins = []

    def load(self, module):
        self.cdb.logger.logger.info("Loading plugins from the module {}...".format(module.__name__))
        for plugin in inspect.getmembers(module, inspect.isclass):
            if issubclass(plugin[1], Plugin) and not plugin[1] is Plugin:
                print("\t" + plugin[1].__name__)
                self.cdb.plugins.append(plugin[1](self.cdb))

    def load_all(self):
        self.cdb.logger.logger.info("#=== PLUGIN LOADING ===#")
        for plugin_name in os.listdir("plugins"):
            if plugin_name.endswith(".py"):
                try:
                    module = importlib.import_module("plugins." + plugin_name[:-3])
                    self.load(module)
                # except ModuleNotFoundError:
                except ImportError as e:
                    print(e)
                    pass
        self.cdb.logger.logger.info("============")
