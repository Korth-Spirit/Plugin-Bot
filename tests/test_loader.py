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
from unittest.mock import Mock, patch

from plugin_bot.plugin import PluginData, PluginLoader
from pytest import raises


def test_load() -> None:
    """
    Test the load plugins method.
    """
    plugin_loader = PluginLoader(
        injector=Mock(),
        bus=Mock(),
        finder=Mock()
    )

    plugin_loader.load(
        plugin_data=PluginData(
            name='test',
            class_=Mock(),
            module=Mock()
        )
    )

    assert len(plugin_loader._plugins) == 1

def test_load_raises_value_error_on_duplicate() -> None:
    """
    Test that the load method raises a ValueError on duplicate.
    """
    plugin_loader = PluginLoader(
        injector=Mock(),
        bus=Mock(),
        finder=Mock()
    )
    plugin_data = PluginData(
        name='test',
        class_=object,
        module=object
    )

    plugin_loader.load(plugin_data)

    with raises(ValueError):
        plugin_loader.load(plugin_data)
    
