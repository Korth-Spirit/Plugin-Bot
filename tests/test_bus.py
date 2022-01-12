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
from unittest.mock import Mock

from korth_spirit import CallBackEnum, EventEnum
from plugin_bot.plugin import PluginBus
from pytest import fixture


@fixture
def plugin_bus() -> PluginBus:
    """
    The fixture for the plugin bus.

    Returns:
        PluginBus: The plugin bus.
    """
    return PluginBus(Mock())

def test_register_generic_plugin(plugin_bus: PluginBus) -> None:
    """
    Test the register plugin method.

    Args:
        plugin_bus (PluginBus): The plugin bus.
    """
    plugin_bus.register_plugin(Mock())

    assert not plugin_bus.instance.subscribe.called
    assert len(plugin_bus._subscribers) == 1

def test_register_plugins(plugin_bus: PluginBus) -> None:
    """
    Test the register plugins method.

    Args:
        plugin_bus (PluginBus): The plugin bus.
    """
    plugin_bus.register_plugins([Mock()])

    assert len(plugin_bus._subscribers) == 1

def test_unregister_plugin(plugin_bus: PluginBus) -> None:
    """
    Test the unregister plugin method.

    Args:
        plugin_bus (PluginBus): The plugin bus.
    """
    plugin_bus.unregister_plugin(Mock())

    assert plugin_bus.instance.unsubscribe.called

def test_unregister_plugins(plugin_bus: PluginBus) -> None:
    """
    Test the unregister plugins method.

    Args:
        plugin_bus (PluginBus): The plugin bus.
    """
    plugin_bus.unregister_plugins([Mock()])

    assert plugin_bus.instance.unsubscribe.called

def test_register_aw_plugin(plugin_bus: PluginBus) -> None:
    """
    Test the register aw plugin method.

    Args:
        plugin_bus (PluginBus): The plugin bus.
    """
    plugin_bus.register_plugin(Mock(
        on_event=EventEnum.AW_EVENT_AVATAR_ADD,
        handle_event=Mock(),
    ))

    assert plugin_bus.instance.subscribe.called