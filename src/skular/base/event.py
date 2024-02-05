from ..models.qdata import QData


class BaseHandler:
    def __init__(self, data: dict):
        self._data: QData = data
