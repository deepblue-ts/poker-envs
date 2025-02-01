import requests
from requests.models import Response
from rich import print

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
