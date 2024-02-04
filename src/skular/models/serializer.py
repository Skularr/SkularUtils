from pydantic import BaseModel


class Serializer(BaseModel):
    def __init__(self, **kwargs):
        if '_id' in kwargs:
            super().__init__(id=str(kwargs.pop('_id')), **kwargs)
        else:
            super().__init__(**kwargs)
