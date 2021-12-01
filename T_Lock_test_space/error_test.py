from typing import Any


class ValidationError(Exception):
    def __init__(self, message='hello'):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


raise ValidationError
