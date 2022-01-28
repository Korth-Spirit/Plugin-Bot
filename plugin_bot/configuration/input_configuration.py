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
from functools import cache

from korth_spirit.coords import Coordinates


class InputConfiguration:
    @cache
    def get_bot_name(self) -> str:
        """
        Returns the name of the bot.

        Returns:
            str: The name of the bot.
        """
        return input("Bot name: ")

    @cache
    def get_citizen_number(self) -> int:
        """
        Returns the citizen number of the owner of the bot.

        Returns:
            int: The citizen number of the owner of the bot.
        """
        while True:
            citizen_number = input("Citizen number: ")
            if citizen_number.isnumeric():
                return int(citizen_number)
            print("Invalid citizen number.")

    @cache
    def get_password(self) -> str:
        """
        Returns the priviledge password of the owner of the bot.

        Returns:
            str: The priviledge password of the owner of the bot.
        """
        return input("Password: ")

    @cache
    def get_world_name(self) -> str:
        """
        Returns the name of the world the bot will enter.

        Returns:
            str: The name of the world the bot will enter.
        """
        return input("World name: ")

    @cache
    def get_world_coordinates(self) -> Coordinates:
        """
        Returns the coordinates of the world the bot will enter.

        Returns:
            tuple: The coordinates where the bot will enter.
        """
        while True:
            x, y, z = input(
                "World coordinates (x, y, z): "
            ).replace(" ", "").split(",")

            if x.isnumeric() and y.isnumeric() and z.isnumeric():
                return Coordinates(
                    int(x), int(y), int(z)
                )
            print("Invalid coordinates.")

    @cache
    def get_plugin_path(self) -> str:
        """
        Returns the path where the plugins are stored.

        Returns:
            str: The path where the plugins are stored.
        """
        return input("Plugin path: ")
