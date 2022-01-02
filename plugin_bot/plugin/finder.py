# Copyright (c) 2021-2022 Johnathan P. Irvin
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
from importlib import import_module, reload
from os import listdir
from typing import Iterable

from .plugin import Plugin, PluginData


class PluginFinder:
    """
    Loads the data related to all the plugins.
    """
    
    def __init__(self, plugin_path: str) -> None:
        """
        Initializes the plugin loader.

        Args:
            plugin_path (str): The path to the plugins.
        """
        self._path: str = plugin_path

    def find_plugins(self) -> Iterable[PluginData]:
        """
        Loads plugins from the specified path.

        Returns:
            List[PluginData]: The plugins.
        """
        self._plugins = []
        for plugin_file in listdir(self._path):
            if not plugin_file.endswith(".py"):
                continue

            for plugin in self._file_to_plugin(plugin_file[:-3]):
                yield plugin

    def _file_to_plugin(self, name: str) -> Iterable[PluginData]:
        """
        Loads a plugin from the specified file.

        Args:
            name (str): The name of the file to load.

        Returns:
            List[PluginData]: The plugins.
        """
        plugin_module = import_module(f"{self._path}.{name}")
        reload(plugin_module)

        plugin_classes = [
            getattr(plugin_module, export) for export in dir(plugin_module)
            if (
                not export.startswith("_") and
                getattr(plugin_module, export) != type and
                issubclass(getattr(plugin_module, export), Plugin)
            )
        ]

        for plugin_class in plugin_classes:
            yield PluginData(
                name=name,
                module=plugin_module,
                class_=plugin_class
            )
