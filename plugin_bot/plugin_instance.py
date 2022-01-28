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
from korth_spirit import Instance, aw_wait

from .configuration import Configuration
from .plugin import PluginBus, PluginFinder, PluginInjector, PluginLoader


class PluginInstance(Instance):
    def __init__(self, configuration: Configuration):
        """
        Initializes a new instance of the PluginInstance class.

        Args:
            configuration (Configuration): The configuration of the bot.
        """        
        super().__init__(
            name=configuration.get_bot_name(),
        )
        self._configuration: Configuration = configuration
        self._bus: PluginBus = PluginBus(instance=self)
        self._loader: PluginLoader = PluginLoader(
            injector = PluginInjector(
                dependencies= {
                    Instance: self,
                    "publish": self._bus.publish,
                }
            ),
            bus = self._bus,
            finder = PluginFinder(
                plugin_path=configuration.get_plugin_path(),
            ),
        )

    def __enter__(self) -> "Instance":
        """
        Initializes the instance.

        Returns:
            Instance: The instance.
        """
        return super().__enter__().login(
            citizen_number=self._configuration.get_citizen_number(),
            password=self._configuration.get_password()
        ).enter_world(
            world_name=self._configuration.get_world_name()
        ).move_to(
            coords=self._configuration.get_world_coordinates()
        )

    def manage_plugins(self) -> bool:
        """
        Manages the plugins.

        Returns:
            bool: True if the plugins were managed successfully, otherwise False.
        """
        self._loader.reload()
        aw_wait(100)
        return True
