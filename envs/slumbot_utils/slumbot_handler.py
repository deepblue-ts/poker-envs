import requests
from requests.models import Response
from rich import print
import time
from typing import Literal
from typing import Optional


class SlumbotHandler:
    def __init__(
        self,
        username: str,
        password: str,
        base_url: str = "slumbot.com",
    ) -> None:
        self.username: str = username
        self.password: str = password
        self.base_url: str = base_url
        self.current_token: Optional[str] = None

    def set_current_token(self, token: str) -> None:
        self.current_token = token

    def login(self) -> dict[str, str]:
        response: dict[str, str] = self.post2slumbot(endpoint_name="login")
        self.set_current_token(token=response["token"])
        return response

    def create_new_hand(self) -> dict[str, str]:
        for _ in range(10):
            _ = self.login()
            response: dict[str, str] = self.post2slumbot(endpoint_name="new_hand")
            done: bool = self._judge_game_ended(response=response)
            if not done:
                break
        if done:
            raise ValueError("Failed to start new hand after 10 trials.")
        return response

    def action(
        self, action: Literal["f", "c", "k", "b"], amount: int
    ) -> dict[str, str]:
        return self.post2slumbot(endpoint_name="act", action=action, amount=amount)

    def post2slumbot(
        self,
        endpoint_name: Literal["login", "new_hand", "act"],
        action: Optional[Literal["f", "c", "k", "b"]] = None,
        amount: Optional[int] = None,
    ) -> dict[str, str]:
        url: str = f"https://{self.base_url}/api/{endpoint_name}"
        payload: dict[str, str] = {}
        if endpoint_name == "login":
            payload = {"username": self.username, "password": self.password}
        else:
            payload = {"token": self.current_token}
            if endpoint_name == "act":
                if action is None:
                    raise ValueError("Specify 'action' to take action.")
                incr: str = self._convert_action2incr(action=action, amount=amount)
                payload["incr"] = incr
        time.sleep(1)
        response: Response = requests.post(url, headers={}, json=payload)
        if response.status_code != 200:
            raise ValueError(
                f"Failed to post. Maybe you tried to take action even though the game ended.\n"
                + f"status code:{response.status_code} response:{response.text}"
            )
        return response.json()

    def _judge_game_ended(self, response: dict[str, str]) -> bool:
        pass

    def _convert_action2incr(
        self, action: Literal["f", "c", "k", "b"], amount: int
    ) -> str:
        pass
