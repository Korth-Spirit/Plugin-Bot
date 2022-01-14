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
from typing import Any, Callable, Tuple, Type
from unittest.mock import patch

from plugin_bot.plugin import PluginData, PluginInjector
from pytest import fixture, mark


class FakeClass:
    def __init__(self, string: str):
        """
        Constructs the class.

        Args:
            string (str): The string to inject.
        """        
        self.string = string

    def get_number(self, number: int) -> int:
        """
        Gets the number from the function.

        Args:
            number (int): The number to get.

        Returns:
            int: The number from the function.
        """
        return number

    def get_second_number(self, number: int) -> int:
        """
        Get the number from the function.

        Args:
            number (int): The number to get.

        Returns:
            int: The number from the function.
        """
        return number

    def get_string(self, string: str) -> str:
        """
        Gets the string from the function.

        Args:
            string (str): The string to get.

        Returns:
            str: The string from the function.
        """
        return string

    def get_constructor_string(self) -> str:
        """
        Gets the string from the constructor.

        Returns:
            str: The string from the constructor.
        """
        return self.string

    def get_positional_argument(self, positional: str = '') -> str:
        """
        Gets the positional argument from the function.

        Args:
            positional (str): The positional argument to get.

        Returns:
            str: The positional argument from the function.
        """
        return positional

    def get_no_annotation_positional(self, positional = '') -> str:
        """
        Get the positional argument from the function.

        Args:
            positional (str, optional): [description]. Defaults to ''.

        Returns:
            str: The positional argument from the function.
        """
        return positional

    def get_no_annotation(self, positional) -> str:
        """
        The function with no annotation.

        Args:
            positional (str): The argument.

        Returns:
            str: The argument.
        """
        return positional

    def get_uninjectable_int(self, number) -> int:
        """
        Get the number from the function.

        Args:
            number (int): The number to get.

        Returns:
            int: The number from the function.
        """
        return number

    def test_mixed(self, number: int, positional = 'unintended') -> Tuple[int, str]:
        """
        Test the mixed arguments.

        Args:
            number (int): The number.
            positional (str): The unannotated argument.

        Returns:
            Tuple(int, str): The number and unannotated argument.
        """
        return number, positional

@fixture
def injector() -> PluginInjector:
    """
    Fixture for the injector.
    """
    return PluginInjector(
        dependencies={
            str: 'string',
            int: 555,
            'positional': 'positional',
        }
    )

@mark.parametrize('dependency, value', [
    (str, 'string'),
    (int, 555),
    ('positional', 'positional'),
])
def test_get_dependency(injector: PluginInjector, dependency: Type, value: Any) -> None:
    """
    Test the get dependency method.

    Args:
        injector (PluginInjector): The injector to test.
        dependency (Type): The dependency to test.
        value (Any): The value to test.
    """
    assert injector.get_dependency(dependency) == value

@mark.parametrize('dependency, value', [
    (str, 'changed'),
    (int, 777),
    ('positional', 'changed'),
])
def test_set_dependency(injector: PluginInjector, dependency: Type, value: Any) -> None:
    """
    Test the set dependency method.

    Args:
        injector (PluginInjector): The injector to test.
        dependency (Type): The dependency to test.
        value (Any): The value to test.
    """
    assert injector.set_dependency(
        dependency=dependency,
        value=value
    ).get_dependency(
        dependency=dependency
    ) == value

@mark.parametrize('function, return_value', [
    (FakeClass.get_number, 555),
    (FakeClass.get_second_number, 555),
    (FakeClass.get_string, 'string'),
    (FakeClass.get_positional_argument, 'positional'),
    (FakeClass.get_no_annotation_positional, 'positional'),
    (FakeClass.get_no_annotation, 'positional'),
])
def test_injected_functions(injector: PluginInjector, function: Callable, return_value: Any) -> None:
    """
    Test the inject functions method.

    Args:
        injector (PluginInjector): The injector to test.
        function (Callable): The function to test.
        return_value (Any): The return value to test.
    """
    injector.inject(PluginData(
        name='test',
        class_=FakeClass,
        module=None,
    ))

    assert function(FakeClass(), return_value) == return_value

@mark.parametrize('function, return_value', [
    (FakeClass.get_number, 555),
    (FakeClass.get_string, 'string'),
    (FakeClass.get_positional_argument, 'positional'),
    (FakeClass.get_no_annotation_positional, 'positional'),
])
def test_functions_before_injection(function: Callable, return_value: Any) -> None:
    """
    Test the functions before injection method.

    Args:
        function (Callable): The function to test.
        return_value (Any): The return value to test.
    """
    assert function(FakeClass(), return_value) == return_value

def test_uninjectable_function(injector: PluginInjector) -> None:
    """
    Test the uninjectable function.

    Args:
        injector (PluginInjector): The injector to test.
    """
    injector.inject(PluginData(
        name='test',
        class_=FakeClass,
        module=None,
    ))

    assert FakeClass().get_uninjectable_int(777) == 777

@mark.parametrize('function, return_value', [
    (FakeClass.get_number, 555),
    (FakeClass.get_second_number, 555),
    (FakeClass.get_string, 'string'),
    (FakeClass.get_positional_argument, 'positional'),
    (FakeClass.get_no_annotation_positional, 'positional'),
])
def test_inject_all(injector: PluginInjector, function: Callable, return_value: Any) -> None:
    """
    Test the inject all method.

    Args:
        injector (PluginInjector): The injector to test.
        function (Callable): The function to test.
        return_value (Any): The return value to test.
    """
    injector.inject_all([
        PluginData(
            name='test',
            class_=FakeClass,
            module=None,
        ),
    ])

    assert function(FakeClass(), return_value) == return_value

def test_mixed_arguments(injector: PluginInjector) -> None:
    """
    Test the mixed arguments.

    Args:
        injector (PluginInjector): The injector to test.
    """
    injector.inject(PluginData(
        name='test',
        class_=FakeClass,
        module=None,
    ))

    assert FakeClass().test_mixed(number=777, positional='changed') == (777, 'changed')
