from abc import ABC, abstractmethod
from typing import Protocol

class AbstractClientState(Protocol):
    def update(self):
        ...