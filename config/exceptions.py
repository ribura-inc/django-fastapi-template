from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Not found.") -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, detail)


class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad request.") -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, detail)


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Unauthorized.") -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail)


class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Forbidden.") -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, detail)


class ConflictException(HTTPException):
    def __init__(self, detail: str = "Conflict.") -> None:
        super().__init__(status.HTTP_409_CONFLICT, detail)
