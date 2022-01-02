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
from unittest.mock import patch

from plugin_bot.plugin import PluginData, PluginInjector


def test_has_dependencies() -> None:
    """
    Test the has dependencies method.
    """
    injector = PluginInjector(
        dependencies={
            str: 'string',
        }
    )

    assert injector.has_dependency(str)
    assert not injector.has_dependency(int)

def test_get_dependency() -> None:
    """
    Test the get dependency method.
    """
    injector = PluginInjector(
        dependencies={
            str: 'string',
        }
    )

    assert injector.get_dependency(str) == 'string'
    assert injector.get_dependency(int) is None

def test_set_dependency() -> None:
    """
    Test the set dependency method.
    """
    injector = PluginInjector(
        dependencies={
            str: 'string',
        }
    )

    injector.set_dependency(int, 555)
    assert injector.get_dependency(int) == 555

def test_inject_functions() -> None:
    """
    Test the inject functions method.
    """
    injector = PluginInjector(
        dependencies={
            str: 'string',
        }
    )

    with patch(
        'plugin_bot.plugin.PluginInjector._inject_functions',
    ) as patched:
        injector.inject(
            PluginData(
                name='test',
                class_=object,
                module=object,
            )
        )

        assert patched.call_count == 1

def test_inject_all() -> None:
    """
    Test the inject functions method with dependencies.
    """
    injector = PluginInjector(
        dependencies={
            str: 'string',
        }
    )

    with patch(
        'plugin_bot.plugin.PluginInjector._inject_functions',
    ) as patched:
        injector.inject_all(
            [
                PluginData(
                    name='test',
                    class_=object,
                    module=object,
                )
            ]
        )

        assert patched.call_count == 1

def test_inject_functions() -> None:
    """
    Test the inject functions method.
    """
    injector = PluginInjector(
        dependencies={
            str: 'string',
        }
    )

    class TestClass:
        def __init__(self, string: str):
            self.string = string

        def uninjectable(self, number: int) -> int:
            return number

    injector._inject_functions(
        PluginData(
            name='test',
            class_=TestClass,
            module=TestClass,
        )
    )

    assert TestClass().string == 'string'
    assert TestClass().uninjectable(1) == 1
