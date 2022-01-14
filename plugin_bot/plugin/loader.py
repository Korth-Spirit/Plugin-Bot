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
from typing import List

from .bus import PluginBus
from .finder import PluginFinder
from .injector import PluginInjector
from .plugin import Plugin, PluginData


class PluginLoader:
    def __init__(self, injector: PluginInjector, bus: PluginBus, finder: PluginFinder) -> None:
        """
        Initialize the plugin loader.

        Args:
            injector (PluginInjector): The dependency injector.
            bus (PluginBus): The event bus.
            finder (PluginFinder): The plugin finder.
        """
        self._plugins: List[Plugin] = []
        self._injector = injector
        self._bus = bus
        self._finder = finder

    def load(self, plugin_data: PluginData) -> "PluginLoader":
        """
        Load a plugin.

        Raises:
            ValueError: If the plugin could not be loaded.

        Args:
            plugin_data (PluginData): The plugin data.
        """
        if plugin_data.class_ in [type(p) for p in self._plugins]:
            raise ValueError(f"Plugin {plugin_data.class_} is already loaded.")

        plugin = self._injector.inject(plugin_data)
        plugin = plugin_data.class_()
        self._bus.register_plugin(plugin)
        
        self._plugins.append(plugin)

        return self

    def load_all(self) -> "PluginLoader":
        """
        Load all plugins.

        Args:
            plugins (List[PluginData]): The list of plugins.
        """
        for plugin_data in self._finder.find_plugins():
            try:
                self.load(plugin_data)
            except ValueError:
                pass

        return self

    def plugins(self) -> List[Plugin]:
        """
        Get the loaded plugins.

        Returns:
            List[Plugin]: The loaded plugins.
        """
        return self._plugins

    def unload(self, plugin: Plugin) -> "PluginLoader":
        """
        Unload a plugin.

        Args:
            plugin (Plugin): The plugin.
        """
        if plugin not in self._plugins:
            raise ValueError(f"Plugin {plugin} is not loaded.")

        self._bus.unregister_plugin(plugin)
        self._plugins.remove(plugin)

        return self
    
    def unload_all(self) -> "PluginLoader":
        """
        Unload all plugins.
        """
        self._bus.unregister_plugins(self._plugins)
        self._plugins = []

        return self

    def reload(self) -> "PluginLoader":
        """
        Reload all plugins.
        """
        self.unload_all()
        self.load_all()

        return self
