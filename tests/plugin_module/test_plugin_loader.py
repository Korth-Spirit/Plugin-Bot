from unittest.mock import Mock, patch

import pytest
from plugin_bot.plugin import PluginLoader


def test_load_plugins():
    """
    Tests the load_plugins method.
    """
    with patch("plugin_bot.plugin.loader.listdir") as listdir:
        listdir.return_value = ["test.py"]
        plugin_loader = PluginLoader("test")

        with patch("plugin_bot.plugin.loader.import_module") as import_module:
            import_module.return_value = Mock()
            plugin_loader.load_plugins()

            assert 1 == len(plugin_loader.get_plugins())
        
def test_ignores_non_python_files():
    """
    Tests that non-python files are ignored.
    """
    with patch("plugin_bot.plugin.loader.listdir") as listdir:
        listdir.return_value = ["test.py", "test.txt"]
        plugin_loader = PluginLoader("test")

        with patch("plugin_bot.plugin.loader.import_module") as import_module:
            import_module.return_value = Mock()
            plugin_loader.load_plugins()

            assert 1 == len(plugin_loader.get_plugins())

def test_get_plugins_before_loading():
    """
    Tests that get_plugins returns an empty list before loading.
    """
    plugin_loader = PluginLoader("test")

    assert 0 == len(plugin_loader.get_plugins())

def test_get_plugins_after_loading():
    """
    Tests that get_plugins returns the plugins after loading.
    """
    with patch("plugin_bot.plugin.loader.listdir") as listdir:
        listdir.return_value = ["test.py"]
        plugin_loader = PluginLoader("test")

        with patch("plugin_bot.plugin.loader.import_module") as import_module:
            import_module.return_value = Mock()
            plugin_loader.load_plugins()

            assert 1 == len(plugin_loader.get_plugins())

def test_get_plugin_by_name():
    """
    Tests that get_plugin returns the plugin with the specified name.
    """
    with patch("plugin_bot.plugin.loader.listdir") as listdir:
        listdir.return_value = ["test.py"]
        plugin_loader = PluginLoader("test")

        with patch("plugin_bot.plugin.loader.import_module") as import_module:
            import_module.return_value = Mock()
            plugin_loader.load_plugins()

            assert "test" == plugin_loader.get_plugin("test").name

def test_get_plugin_throw_exception_when_plugin_not_found():
    """
    Tests that get_plugin throws an exception when the plugin is not found.
    """
    with patch("plugin_bot.plugin.loader.listdir") as listdir:
        listdir.return_value = ["test.py"]
        plugin_loader = PluginLoader("test")

        with patch("plugin_bot.plugin.loader.import_module") as import_module:
            import_module.return_value = Mock()
            plugin_loader.load_plugins()

            with pytest.raises(LookupError):
                plugin_loader.get_plugin("test2")
    
def test_get_plugin_throw_exception_when_plugin_not_loaded():
    """
    Tests that get_plugin throws an exception when the plugin is not loaded.
    """
    with patch("plugin_bot.plugin.loader.listdir") as listdir:
        listdir.return_value = ["test.py"]
        plugin_loader = PluginLoader("test")

        with patch("plugin_bot.plugin.loader.import_module") as import_module:
            import_module.return_value = Mock()
            with pytest.raises(LookupError):
                plugin_loader.get_plugin("test")

def test_double_loading_plugins():
    """
    Tests that loading plugins twice does not add any plugins.
    """
    with patch("plugin_bot.plugin.loader.listdir") as listdir:
        listdir.return_value = ["test.py"]
        plugin_loader = PluginLoader("test")

        with patch("plugin_bot.plugin.loader.import_module") as import_module:
            import_module.return_value = Mock()
            plugin_loader.load_plugins()
            plugin_loader.load_plugins()

            assert 1 == len(plugin_loader.get_plugins())

def test_has_plugin():
    """
    Tests that has_plugin returns true when the plugin is found.
    """
    plugin_loader = PluginLoader("test")

    with patch("plugin_bot.plugin.loader.listdir") as listdir:
        listdir.return_value = ["test.py"]
        with patch("plugin_bot.plugin.loader.import_module") as import_module:
            import_module.return_value = Mock()
            plugin_loader.load_plugins()

            assert plugin_loader.has_plugin("test")

def test_does_not_have_plugin():
    """
    Tests that has_plugin returns false when the plugin is not found.
    """
    plugin_loader = PluginLoader("test")
    
    assert not plugin_loader.has_plugin("test2")

def test_add_plugin():
    """
    Tests that add_plugin adds a plugin.
    """
    plugin_loader = PluginLoader("test")
    with patch("plugin_bot.plugin.loader.import_module") as import_module:
        import_module.return_value = Mock()
        plugin_loader.add_plugin('fake_plugin')

        assert plugin_loader.has_plugin("fake_plugin")

    assert 1 == len(plugin_loader.get_plugins())

def test_get_correct_plugin_when_multiple_plugins_exist():
    """
    Tests that get_plugin returns the correct plugin when multiple plugins exist.
    """
    plugin_loader = PluginLoader("test")
    with patch("plugin_bot.plugin.loader.import_module") as import_module:
        import_module.return_value = Mock()
        plugin_loader.add_plugin('fake_plugin')
        plugin_loader.add_plugin('fake_plugin2')

        assert plugin_loader.get_plugin("fake_plugin").name == "fake_plugin"

def test_already_loaded_plugin():
    """
    Tests that add_plugin does not add a plugin that is already loaded.
    """
    plugin_loader = PluginLoader("test")
    with patch("plugin_bot.plugin.loader.import_module") as import_module:
        import_module.return_value = Mock()
        plugin_loader.add_plugin('fake_plugin')

        with pytest.raises(ValueError):
            plugin_loader.add_plugin('fake_plugin')
    