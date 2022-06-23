from __future__ import annotations
from abc import ABC, abstractmethod


class Utils:
    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    async def start_realisation(self, data) -> None:
        print("Start strategy")
        await self._strategy.do_algorithm(data)
        print("End strategy")


class Strategy(ABC):

    @abstractmethod
    async def do_algorithm(self, data):
        print("empty strategy")
