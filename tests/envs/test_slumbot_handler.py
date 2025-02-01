import pytest
from envs.slumbot_handler import SlumbotHandler

class TestSlumbotHandler:
    def test_init(self):
        slumbot_handler = SlumbotHandler(
            username="test",
            password="test",
        )
        assert slumbot_handler is not None
        assert slumbot_handler.username == "test"
        assert slumbot_handler.password == "test"
        assert slumbot_handler.base_url == "slumbot.com"