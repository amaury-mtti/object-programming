"""
Singleton pattern - refactor of the configuration manager.

Before: every module called load_config(), so config.json was read from
disk 4 times for a single request, and each module had its own copy
(a change made in one module was invisible to the others).

After: ConfigManager.get_instance() always returns the SAME object.
The file is read only once, on the first call, and every module shares
the same data.
"""

import json
from pathlib import Path

# config.json sits next to this file, so the script works from any folder
CONFIG_PATH = Path(__file__).parent / "config.json"


class ConfigManager:
    _instance = None  # class attribute shared by everyone

    def __init__(self, path=CONFIG_PATH):
        # Block "ConfigManager()" once the instance exists:
        # everybody must go through get_instance().
        if ConfigManager._instance is not None:
            raise RuntimeError("Use ConfigManager.get_instance() instead")
        self.load_count = 0
        self._config = self._load(path)

    def _load(self, path):
        with open(path, "r") as f:
            self.load_count += 1
            return json.load(f)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:   # first call: create it (reads the file)
            cls._instance = cls()
        return cls._instance        # next calls: same object, no file read

    def get(self, key, default=None):
        """Read a nested value with a dotted key, e.g. get("database.host")."""
        value = self._config
        for part in key.split("."):
            if not isinstance(value, dict) or part not in value:
                return default
            value = value[part]
        return value

    def set(self, key, new_value):
        """Change a value: every module sees it since they share the instance."""
        parts = key.split(".")
        section = self._config
        for part in parts[:-1]:
            section = section.setdefault(part, {})
        section[parts[-1]] = new_value


# ---------------------------------------------------------------------------
# The four services, now all using the same ConfigManager
# ---------------------------------------------------------------------------
def start_application():
    config = ConfigManager.get_instance()
    print(f"Starting {config.get('app.name')} (debug={config.get('app.debug')})")


def connect_database():
    config = ConfigManager.get_instance()
    print(f"Connecting to database at {config.get('database.host')}:{config.get('database.port')}")


def send_email(to: str, subject: str):
    config = ConfigManager.get_instance()
    print(f"Sending email from {config.get('email.sender')} via {config.get('email.smtp_host')}")


def process_payment(amount: float):
    config = ConfigManager.get_instance()
    print(f"Processing {amount}€ in {config.get('payment.environment')} mode")


if __name__ == "__main__":
    start_application()
    connect_database()
    send_email("user@test.com", "Welcome")
    process_payment(99.99)
    print("config.json was read", ConfigManager.get_instance().load_count, "time(s)")
