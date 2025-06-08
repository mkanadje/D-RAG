from abc import ABC, abstractmethod
from typing import Any, List, Optional


class UIService(ABC):
    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def display_message(self, message: str, role: str) -> None:
        pass

    @abstractmethod
    def get_user_input(self) -> str:
        pass

    @abstractmethod
    def show_build_button(self) -> bool:
        pass
