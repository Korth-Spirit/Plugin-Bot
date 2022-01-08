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
from korth_spirit.coords import Coordinates

from plugin_bot.plugin import (PluginBus, PluginFinder, PluginInjector,
                               PluginLoader)


def main() -> None:
    """
    Main entry point for the application.
    """
    with Instance(
        name=input("Bot Name: "),
    ) as bot:
        bus = PluginBus(instance=bot)
        plugin_loader: PluginLoader = PluginLoader(
            injector = PluginInjector(
                dependencies = {
                    Instance: bot,
                },
            ),
            bus = bus,
            finder = PluginFinder(
                plugin_path="plugins"
            )
        )

        bot.login(
            citizen_number=int(input("Citizen Number: ")),
            password=input("Password: "),
        ).enter_world(
            world_name=input("World Name: "),
        ).move_to(
            Coordinates(
                x=int(input("X: ")),
                y=int(input("Y: ")),
                z=int(input("Z: ")),
            )
        )

        while True:
            plugin_loader.reload()
            aw_wait(10)
