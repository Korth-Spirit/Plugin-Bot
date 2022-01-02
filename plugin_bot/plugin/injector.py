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
from functools import partialmethod
from typing import Dict, Iterable, Type

from .plugin import PluginData


class PluginInjector:
    """
    Dependency injector that inspects the plugin class for dependencies, and injects them into the plugin.
    Functions of the plugin may also be annotated with dependencies, and these will be injected into the plugin.
    The plugin injector stores a list of dependencies and their corresponding values.
    """
    def __init__(self, dependencies: Dict[Type, object] = {}):
        """
        Initialize the plugin injector.

        Args:
            dependencies (Dict[Type, object]): The dependencies to inject into the plugin.
        """        
        self._dependencies: Dict = dependencies

    def inject(self, plugin: PluginData) -> "PluginInjector":
        """
        Inject dependencies into the plugin.

        Args:
            plugin (PluginData): The plugin to inject dependencies into.
        
        Returns:
            PluginInjector: The plugin injector.
        """
        self._inject_functions(plugin)

        return self

    def inject_all(self, plugins: Iterable[PluginData]) -> "PluginInjector":
        """
        Inject dependencies into all of the plugins.

        Args:
            plugins (Iterable[PluginData]): The plugins to inject dependencies into.

        Returns:
            PluginInjector: The plugin injector.
        """
        for plugin in plugins:
            self.inject(plugin)

        return self

    def _inject_functions(self, plugin: PluginData):
        """
        Inject dependencies into the plugin functions.

        Args:
            plugin (PluginData): The plugin to inject dependencies into.
        """
        for function in plugin.class_.__dict__.values():
            if not hasattr(function, '__annotations__'):
                continue

            injectable = {
                key: self.get_dependency(value)
                for key, value in function.__annotations__.items()
                if value in self._dependencies.keys()
            }
            uninjectable = {
                key: value
                for key, value in function.__annotations__.items()
                if value not in self._dependencies.keys() and
                "return" not in key
            }

            if not injectable:
                continue

            injected_function = partialmethod(function, **uninjectable, **injectable)

            setattr(plugin.class_, function.__name__, injected_function)

    def has_dependency(self, dependency: Type) -> bool:
        """
        Checks if the injector has a dependency.

        Args:
            dependency (Type): The dependency to check for.

        Returns:
            bool: True if the dependency exists, False otherwise.
        """
        return dependency in self._dependencies

    def get_dependency(self, dependency: Type) -> object:
        """
        Gets the dependency from the injector.

        Args:
            dependency (Type): The dependency to get.

        Returns:
            object: The dependency.
        """
        return self._dependencies.get(dependency)

    def set_dependency(self, dependency: Type, value: object):
        """
        Sets the dependency in the injector.

        Args:
            dependency (Type): The dependency to set.
            value (object): The value to set the dependency to.
        """
        self._dependencies[dependency] = value
