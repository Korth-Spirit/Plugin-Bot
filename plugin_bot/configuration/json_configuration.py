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
import json
from functools import cache

from korth_spirit.coords import Coordinates


class JsonConfiguration:
    def __init__(self, config_file: str):
        """
        Loads a configuration file and stores the values in the class.

        Args:
            config_file (str): The path to the configuration file.
        """
        with open(config_file, "r") as file:
            self._config: dict = json.load(file)

    @cache
    def get_bot_name(self) -> str:
        """
        Returns the name of the bot.

        Raises:
            KeyError: If the bot name is not specified in the configuration file.

        Returns:
            str: The name of the bot.
        """
        return self._config["bot_name"]

    @cache
    def get_citizen_number(self) -> int:
        """
        Returns the citizen number of the owner of the bot.

        Raises:
            KeyError: If the citizen number is not specified in the configuration file.

        Returns:
            int: The citizen number of the owner of the bot.
        """
        return self._config["citizen_number"]

    @cache
    def get_password(self) -> str:
        """
        Returns the priviledge password of the owner of the bot.

        Raises:
            KeyError: If the password is not specified in the configuration file.

        Returns:
            str: The priviledge password of the owner of the bot.
        """
        return self._config["password"]

    @cache
    def get_world_name(self) -> str:
        """
        Returns the name of the world the bot will enter.

        Raises:
            KeyError: If the world name is not specified in the configuration file.

        Returns:
            str: The name of the world the bot will enter.
        """
        return self._config["world_name"]

    @cache
    def get_world_coordinates(self) -> Coordinates:
        """
        Returns the coordinates of the world the bot will enter.

        Raises:
            KeyError: If the world coordinates are not specified in the configuration file.

        Returns:
            Coordinates: The coordinates where the bot will enter.
        """
        return Coordinates(
            x=self._config["world_coordinates"]["x"],
            y=self._config["world_coordinates"]["y"],
            z=self._config["world_coordinates"]["z"],
        )

    @cache
    def get_plugin_path(self) -> str:
        """
        Returns the path where the plugins are stored.

        Raises:
            KeyError: If the plugin path is not specified in the configuration file.

        Returns:
            str: The path where the plugins are stored.
        """
        return self._config["plugin_path"]
