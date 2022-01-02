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
from unittest.mock import call, patch

from plugin_bot.plugin import PluginFinder
from pytest import fixture


@fixture
def plugin_finder() -> PluginFinder:
    """
    The fixture for the plugin finder.
    """
    return PluginFinder(plugin_path='tests/plugins')

def test_find_plugins(plugin_finder: PluginFinder) -> None:
    """
    Test the find plugins method.
    """

    with patch(
        'plugin_bot.plugin.finder.listdir',
        return_value=[
            'plugin_a.py',
            'plugin_b.py',
            'invalid.c'
        ]
    ):
        with patch(
            "plugin_bot.plugin.finder.PluginFinder._file_to_plugin",
        ) as patched:
            list(plugin_finder.find_plugins())
            
            patched.assert_has_calls(
                [
                    call('plugin_a'),
                    call().__iter__(),
                    call('plugin_b'),
                    call().__iter__()
                ]
            )
