class NoEventHandlerException(Exception):
    def __init__(self):
        message = "No event handler added"
        super().__init__(message)
