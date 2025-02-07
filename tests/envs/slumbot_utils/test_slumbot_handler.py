import pytest
from envs.slumbot_utils import SlumbotHandler


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
        assert slumbot_handler.current_token is None

    def test_login(self):
        slumbot_handler = SlumbotHandler(
            username="test",
            password="test",
        )
        response = slumbot_handler.login()
        assert response is not None
        assert "token" in response
        assert slumbot_handler.current_token == response["token"]

    def test_create_new_hand(self): # TODO: test refresh_token=False cash
        slumbot_handler = SlumbotHandler(
            username="test",
            password="test",
        )
        response: dict[str, str] = slumbot_handler.create_new_hand(
            refresh_token=True
        )
        assert response is not None
        assert response["old_action"] == ""
        assert (
            response["action"] == "b200" or response["action"] == ""
        )
        assert len(response["hole_cards"]) == 2
        assert len(response["board"]) == 0
        assert "winnings" not in response
        assert "won_pot" not in response
        assert "session_num_hands" not in response
        assert "baseline_winnings" not in response
        assert "session_total" not in response
        assert "session_baseline_total" not in response

    def test_action_f(self): # TODO: test refresh_token=False cash
        slumbot_handler = SlumbotHandler(
            username="test",
            password="test",
        )
        response: dict[str, str] = slumbot_handler.create_new_hand(refresh_token=True)
        response: dict[str, str] = slumbot_handler.action(action="f")
        assert slumbot_handler._judge_game_ended(response) is True
        assert response["old_action"] == "b200"
        assert response["action"] == "b200f"
        assert len(response["hole_cards"]) == 2
        assert len(response["bot_hole_cards"]) == 2
        assert len(response["board"]) == 0

    def test_action_c(self): # TODO: test refresh_token=False cash
        slumbot_handler = SlumbotHandler(
            username="test",
            password="test",
        )
        response: dict[str, str] = slumbot_handler.create_new_hand(refresh_token=True)
        response: dict[str, str] = slumbot_handler.action(action="c")
        assert slumbot_handler._judge_game_ended(response) is False
        assert response["old_action"] == "b200"
        assert response["action"] == "b200c/"
        assert len(response["hole_cards"]) == 2
        assert len(response["board"]) == 3

    def test_action_k(self): # TODO: test refresh_token=False cash
        slumbot_handler = SlumbotHandler(
            username="test",
            password="test",
        )
        response: dict[str, str] = slumbot_handler.create_new_hand(refresh_token=True)
        response: dict[str, str] = slumbot_handler.action(action="k")
        assert response["error_msg"] == "Illegal check"
        response: dict[str, str] = slumbot_handler.create_new_hand(refresh_token=True)
        response: dict[str, str] = slumbot_handler.action(action="c")
        response: dict[str, str] = slumbot_handler.action(action="k")
        assert slumbot_handler._judge_game_ended(response) is False
        assert response["old_action"] == "b200c/"
        assert "b200c/k" in response["action"]
        print(response)
        assert len(response["hole_cards"]) == 2
        if response["action"] == "b200c/kk/":
            assert len(response["board"]) == 4
        else:
            assert len(response["board"]) == 3

    def test_action_b(self): # TODO: test refresh_token=False cash
        slumbot_handler = SlumbotHandler(
            username="test",
            password="test",
        )
        response: dict[str, str] = slumbot_handler.create_new_hand(refresh_token=True)
        response: dict[str, str] = slumbot_handler.action(action="b", amount=400)
        assert response["old_action"] == "b200"
        assert "b200b400" in response["action"]
        if response["action"] == "b200b400f":
            assert slumbot_handler._judge_game_ended(response) is True
        elif "b200b400b" in response["action"]:
            assert slumbot_handler._judge_game_ended(response) is False
            assert len(response["hole_cards"]) == 2
            assert len(response["board"]) == 0
        elif response["action"] == "b200b400c/":
            assert slumbot_handler._judge_game_ended(response) is False
            assert len(response["hole_cards"]) == 2
            assert len(response["board"]) == 3
        else:
            raise ValueError(f"Unexpected response: {response}")
        response: dict[str, str] = slumbot_handler.create_new_hand(refresh_token=True)
        response: dict[str, str] = slumbot_handler.action(action="c")
        response: dict[str, str] = slumbot_handler.action(action="b", amount=400)
        assert response["old_action"] == "b200c/"
        assert "b200c/b400" in response["action"]
        if response["action"] == "b200c/b400f":
            assert slumbot_handler._judge_game_ended(response) is True
        elif "b200c/b400b" in response["action"]:
            assert slumbot_handler._judge_game_ended(response) is False
            assert len(response["hole_cards"]) == 2
            assert len(response["board"]) == 3
        elif response["action"] == "b200c/b400c/":
            assert slumbot_handler._judge_game_ended(response) is False
            assert len(response["hole_cards"]) == 2
            assert len(response["board"]) == 4
