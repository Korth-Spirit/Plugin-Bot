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
import inspect
from functools import partialmethod, update_wrapper
from typing import Callable, Dict, Iterable, Type

from .plugin import PluginData


class PluginInjector:
    """
    Dependency injector that inspects the plugin class for dependencies, and injects them into the plugin.
    Functions of the plugin may also be annotated with dependencies, and these will be injected into the plugin.
    The plugin injector stores a list of dependencies and their corresponding values.
    """

    def _yield_functions(self, plugin: PluginData):
        """
        Yields the methods of the plugin.

        Args:
            plugin (PluginData): The plugin to yield functions of.
        """
        for name, function in inspect.getmembers(plugin.class_, inspect.isfunction):
            yield function

    def _get_annotated_injectables(self, func: Callable) -> Dict:
        """
        Gets the annotated injectables from the function.

        Args:
            func (Callable): The function to inject dependencies into.

        Returns:
            Dict: The dependencies to inject into the function.
        """
        return {
            arg_name: self.get_dependency(arg_type)
            for arg_name, arg_type in func.__annotations__.items()
            if arg_type in self._dependencies.keys()
            and arg_name != 'return'
        }

    def _get_named_injectables(self, func: Callable) -> Dict:
        """
        Gets the named injectables from the function.

        Args:
            func (Callable): The function to inject named arguments into.

        Returns:
            Dict: The named arguments to inject into the function.
        """
        full_arg_spec = inspect.getfullargspec(func)
        args = full_arg_spec.args
        args.extend(full_arg_spec.kwonlyargs or [])

        return {
            arg_name: self.get_dependency(arg_name)
            for arg_name in args
            if arg_name in self._dependencies.keys()
        }

    def _inject(self, func: Callable, injectables: Dict) -> Callable:
        """
        Inject the dependencies into a function.

        Args:
            func (Callable): The function to inject dependencies into.
            injectables (Dict): The dependencies to inject into the function.

        Returns:
            Callable: The function with the injected dependencies.
        """
        return update_wrapper(partialmethod(func, **injectables), func)

    def __init__(self, dependencies: Dict[Type, object]):
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
        for func in self._yield_functions(plugin):
            injectables = self._get_named_injectables(func)
            injectables.update(self._get_annotated_injectables(func))

            setattr(
                plugin.class_,
                func.__name__,
                self._inject(
                    func=func,
                    injectables=injectables
                )
            )
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

    def get_dependency(self, dependency: Type) -> object:
        """
        Gets the dependency from the injector.

        Args:
            dependency (Type): The dependency to get.

        Returns:
            object: The dependency.
        """
        return self._dependencies.get(dependency)

    def set_dependency(self, dependency: Type, value: object) -> "PluginInjector":
        """
        Sets the dependency in the injector.

        Args:
            dependency (Type): The dependency to set.
            value (object): The value to set the dependency to.

        Returns:
            PluginInjector: The plugin injector.
        """
        self._dependencies[dependency] = value

        return self
