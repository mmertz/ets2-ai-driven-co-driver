
class AIProcessingError(Exception):
    """
    Exception raised for errors that occur during AI processing.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"AIProcessingError: {self.message}"
