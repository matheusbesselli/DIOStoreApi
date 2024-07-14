from fastapi import HTTPException


class BaseException(Exception):
    message: str = "Internal Server Error"

    def __init__(self, message: str | None = None) -> None:
        if message:
            self.message = message


class NotFoundException(BaseException):
    message = "Not Found"

class InsertionError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)