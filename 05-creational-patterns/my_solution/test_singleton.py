import pytest

from singleton import ConfigManager


def test_same_instance():
    assert ConfigManager.get_instance() is ConfigManager.get_instance()


def test_file_read_only_once():
    for _ in range(5):
        ConfigManager.get_instance()
    assert ConfigManager.get_instance().load_count == 1


def test_get_nested_values():
    config = ConfigManager.get_instance()
    assert config.get("database.host") == "localhost"
    assert config.get("database.port") == 5432
    assert config.get("app.debug") is True
    assert config.get("does.not.exist", "default") == "default"


def test_shared_state():
    ConfigManager.get_instance().set("app.debug", False)
    assert ConfigManager.get_instance().get("app.debug") is False
    ConfigManager.get_instance().set("app.debug", True)  # put it back


def test_direct_creation_blocked():
    ConfigManager.get_instance()
    with pytest.raises(RuntimeError):
        ConfigManager()
