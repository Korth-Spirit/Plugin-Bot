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
from typing import Any
from unittest.mock import Mock

from korth_spirit import EventEnum
from plugin_bot.plugin import PluginBus
from pytest import fixture


class FakePlugin:
    """
    A fake plugin.
    """
    def __init__(self, event: Any):
        """
        Constructs the class.

        Args:
            event (Any): The event to inject.
        """
        self.event = event

    @property
    def on_event(self) -> Any:
        """
        Event to listen for.

        Returns:
            Any: The event.
        """
        return self.event

    def handle_event(self, event: Any) -> Any:
        """
        Handles the event.

        Args:
            event (Any): The event to handle.
        
        Returns:
            Any: The event.
        """
        return event

@fixture
def aw_plugin() -> FakePlugin:
    """
    A fake plugin.
    """
    return FakePlugin(EventEnum.AW_EVENT_AVATAR_ADD)

@fixture
def generic_plugin() -> FakePlugin:
    """
    A generic plugin.
    """
    return FakePlugin('generic')

@fixture
def plugin_bus() -> PluginBus:
    """
    The fixture for the plugin bus.

    Returns:
        PluginBus: The plugin bus.
    """
    return PluginBus(Mock())

def test_register_generic_plugin(plugin_bus: PluginBus, generic_plugin: FakePlugin) -> None:
    """
    Test the register plugin method.

    Args:
        plugin_bus (PluginBus): The plugin bus.
        generic_plugin (FakePlugin): The generic plugin.
    """
    plugin_bus.register_plugin(generic_plugin)

    assert not plugin_bus.instance.subscribe.called
    assert len(plugin_bus._subscribers) == 1
    assert plugin_bus._subscribers == {"generic": [generic_plugin.handle_event]}

def test_register_plugin_twice(plugin_bus: PluginBus, generic_plugin: FakePlugin) -> None:
    """
    Test the register plugin twice method.

    Args:
        plugin_bus (PluginBus): The plugin bus.
        generic_plugin (FakePlugin): The generic plugin.
    """
    plugin_bus.register_plugin(generic_plugin)
    plugin_bus.register_plugin(generic_plugin)

    assert len(plugin_bus._subscribers) == 1
    assert plugin_bus._subscribers == {"generic": [generic_plugin.handle_event]}

def test_register_plugins(plugin_bus: PluginBus, generic_plugin: FakePlugin, aw_plugin: FakePlugin) -> None:
    """
    Test the register plugins method.

    Args:
        plugin_bus (PluginBus): The plugin bus.
        generic_plugin (FakePlugin): The generic plugin.
        aw_plugin (FakePlugin): The aw plugin.
    """
    plugin_bus.register_plugins(
        [generic_plugin, aw_plugin],
    )

    assert len(plugin_bus._subscribers) == 1
    assert plugin_bus._subscribers == {"generic": [generic_plugin.handle_event]}
    assert plugin_bus.instance.subscribe.called_once

def test_unregister_plugin(plugin_bus: PluginBus) -> None:
    """
    Test the unregister plugin method.

    Args:
        plugin_bus (PluginBus): The plugin bus.
    """
    plugin_bus.unsubscribe = Mock()

    plugin_bus.unregister_plugin(Mock())

    assert plugin_bus.unsubscribe.called

def test_unregister_plugins(plugin_bus: PluginBus) -> None:
    """
    Test the unregister plugins method.

    Args:
        plugin_bus (PluginBus): The plugin bus.
    """
    plugin_bus.unsubscribe = Mock()

    plugin_bus.unregister_plugins([Mock()])

    assert plugin_bus._subscribers == {}

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

def test_unregister_aw_plugin(plugin_bus: PluginBus) -> None:
    """
    Test the unregister aw plugin method.

    Args:
        plugin_bus (PluginBus): The plugin bus.
    """
    plugin_bus.unregister_plugin(Mock(
        on_event=EventEnum.AW_EVENT_AVATAR_ADD,
        handle_event=Mock(),
    ))

    assert plugin_bus.instance.unsubscribe.called
