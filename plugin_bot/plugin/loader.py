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
from importlib import import_module
from os import listdir
from typing import List

from .plugin import PluginData


class PluginLoader:
    """
    Loads the data related to all the plugins.
    """
    
    def __init__(self, plugin_path: str) -> None:
        """
        Initializes the plugin loader.

        Args:
            plugin_path (str): The path to the plugins.
        """
        self._plugins: List[PluginData] = []
        self._path: str = plugin_path

    def load_plugins(self) -> "PluginLoader":
        """
        Loads plugins from the specified path.
        """
        self._plugins = []
        for plugin_file in listdir(self._path):
            if not plugin_file.endswith(".py"):
                continue
            self.add_plugin(plugin_file[:-3])
        return self

    def get_plugins(self) -> List[PluginData]:
        """
        Gets the plugins that have been loaded.

        Returns:
            List[PluginData]: The plugins.
        """
        return self._plugins

    def get_plugin(self, name: str) -> PluginData:
        """
        Gets the plugin with the specified name from the loaded plugins.

        Args:
            name (str): The name of the plugin.

        Raises:
            LookupError: If the plugin does not exist.

        Returns:
            PluginData: The plugin.
        """
        for plugin in self._plugins:
            if plugin.name == name:
                return plugin

        raise LookupError(f"Plugin with name {name} not found.")

    def add_plugin(self, name: str) -> None:
        """
        Adds a plugin to the loaded plugins.

        Args:
            name (str): The name of the plugin.

        Raises:
            ValueError: If the plugin already exists.
        """
        if self.has_plugin(name):
            raise ValueError(f"Plugin with name {name} already exists.")
        
        plugin_module = import_module(f"{self._path}.{name}")
        plugin_class = getattr(plugin_module, name)
        self._plugins.append(
            PluginData(
                name=name,
                module=plugin_module,
                class_=plugin_class
            )
        )

    def has_plugin(self, name: str) -> bool:
        """
        Checks if the plugin with the specified name exists.

        Args:
            name (str): The name of the plugin.

        Returns:
            bool: Whether the plugin exists.
        """
        for plugin in self._plugins:
            if plugin.name == name:
                return True

        return False