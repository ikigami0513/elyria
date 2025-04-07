from network.abstract_handler import AbstractHandler
from network.handlers.login_handler import LoginHandler
from typing import Dict


HANDLERS: Dict[str, AbstractHandler] = {
    "login": LoginHandler()
}
