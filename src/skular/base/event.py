from abc import ABC, abstractmethod

from ..models.qdata import QData


class BaseHandler(ABC):
    def __init__(self, data: dict):
        self._data: QData = data

    @abstractmethod
    async def __call__(self):
        ...
