from abc import ABC, abstractmethod
from typing import Protocol

class AbstractClientState(Protocol):
    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def on_enter(self, on_enter_data: dict):
        ...