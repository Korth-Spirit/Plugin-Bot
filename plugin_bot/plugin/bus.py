# Copyright (c) 2021 Johnathan P. Irvin
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from functools import wraps
from typing import List

from korth_spirit import EventEnum, Instance

from .plugin import Plugin


class PluginBus:
    def __init__(self, instance: Instance) -> None:
        """
        Initialize the plugin bus.

        Args:
            instance (Instance): The instance of the bot.
        """        
        self.instance = instance

    def register_plugin(self, plugin: Plugin) -> "PluginBus":
        """
        Register a plugin.

        Args:
            plugin (PluginData): The plugin data.

        Returns:
            PluginBus: The plugin bus.
        """
        self.instance.subscribe(
            event=plugin.on_event,
            subscriber=plugin.handle_event,
        )

    def register_plugins(self, plugins: List[Plugin]) -> "PluginBus":
        """
        Register a list of plugins.

        Args:
            plugins (List[PluginData]): The list of plugins.

        Returns:
            PluginBus: The plugin bus.
        """
        for plugin in plugins:
            self.register_plugin(plugin)
    
    def unregister_plugin(self, plugin: Plugin) -> "PluginBus":
        """
        Unregister a plugin.

        Args:
            plugin (PluginData): The plugin data.

        Returns:
            PluginBus: The plugin bus.
        """
        self.instance.unsubscribe(
            event=plugin.on_event,
            subscriber=plugin.handle_event,
        )

    def unregister_plugins(self, plugins: List[Plugin]) -> "PluginBus":
        """
        Unregister a list of plugins.

        Args:
            plugins (List[PluginData]): The list of plugins.

        Returns:
            PluginBus: The plugin bus.
        """
        for plugin in plugins:
            self.unregister_plugin(plugin)
