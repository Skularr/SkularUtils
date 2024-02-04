from .serializer import Serializer


class Success(Serializer):
    success: bool
    id: str


class SuccessM(Serializer):
    success: bool
    message: str
