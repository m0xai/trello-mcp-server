"""
Custom exceptions for Trello MCP Server.

This module defines a hierarchy of exceptions for handling various error scenarios
in the Trello MCP server, providing clear and actionable error messages.
"""

from typing import Optional


class TrelloMCPError(Exception):
    """Base exception for all Trello MCP errors."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(TrelloMCPError):
    """Raised when input validation fails."""

    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class ResourceNotFoundError(TrelloMCPError):
    """Raised when a requested resource is not found (404)."""

    def __init__(self, resource_type: str, resource_id: str):
        message = f"{resource_type} '{resource_id}' not found. Please verify the ID and try again."
        super().__init__(message, status_code=404)


class UnauthorizedError(TrelloMCPError):
    """Raised when authentication fails (401)."""

    def __init__(
        self,
        message: str = "Invalid API key or token. Please check your credentials in the .env file.",
    ):
        super().__init__(message, status_code=401)


class ForbiddenError(TrelloMCPError):
    """Raised when the user lacks permission to perform an action (403)."""

    def __init__(self, resource_type: str, resource_id: str, action: str = "access"):
        message = f"Permission denied to {action} {resource_type} '{resource_id}'. Check your board/workspace permissions."
        super().__init__(message, status_code=403)


class RateLimitError(TrelloMCPError):
    """Raised when API rate limit is exceeded (429)."""

    def __init__(self, retry_after: Optional[int] = None):
        if retry_after:
            message = f"Trello API rate limit exceeded. Please retry after {retry_after} seconds."
        else:
            message = "Trello API rate limit exceeded. Please wait a moment and try again."
        super().__init__(message, status_code=429)
        self.retry_after = retry_after


class ConflictError(TrelloMCPError):
    """Raised when there's a conflict with the current state (409)."""

    def __init__(self, message: str):
        super().__init__(message, status_code=409)


class BadRequestError(TrelloMCPError):
    """Raised when the request is malformed or invalid (400)."""

    def __init__(self, message: str):
        super().__init__(message, status_code=400)
