"""
Validation service for Trello MCP Server.

This module provides validation functions for verifying resource existence,
permissions, and business rules before executing operations.
"""

import logging
import re
from typing import Optional

import httpx

from server.exceptions import (
    BadRequestError,
    ForbiddenError,
    ResourceNotFoundError,
    UnauthorizedError,
    ValidationError,
)
from server.utils.trello_api import TrelloClient

logger = logging.getLogger(__name__)


class ValidationService:
    """Service for validating Trello resources and permissions."""

    def __init__(self, client: TrelloClient):
        self.client = client

    def validate_id_format(self, resource_id: str, resource_type: str) -> None:
        """
        Validate that a resource ID matches Trello's ID format.

        Args:
            resource_id: The ID to validate
            resource_type: Type of resource (for error messages)

        Raises:
            ValidationError: If the ID format is invalid
        """
        if not resource_id:
            raise ValidationError(f"{resource_type} ID cannot be empty")

        # Trello IDs are 24-character hexadecimal strings
        if not re.match(r"^[a-f0-9]{24}$", resource_id):
            raise ValidationError(
                f"Invalid {resource_type} ID format. Expected 24-character hexadecimal string, got: {resource_id}"
            )

    async def validate_board_exists(self, board_id: str) -> bool:
        """
        Verify that a board exists and the user has access to it.

        Args:
            board_id: The ID of the board to validate

        Returns:
            True if the board exists and is accessible

        Raises:
            ValidationError: If the board ID format is invalid
            ResourceNotFoundError: If the board doesn't exist
            ForbiddenError: If the user doesn't have access
            UnauthorizedError: If authentication fails
        """
        self.validate_id_format(board_id, "Board")

        try:
            logger.debug(f"Validating board exists: {board_id}")
            await self.client.GET(f"/boards/{board_id}", params={"fields": "id,closed"})
            logger.debug(f"Board {board_id} exists and is accessible")
            return True
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ResourceNotFoundError("Board", board_id)
            elif e.response.status_code == 401:
                raise UnauthorizedError()
            elif e.response.status_code == 403:
                raise ForbiddenError("Board", board_id, "access")
            raise

    async def validate_list_exists(self, list_id: str) -> bool:
        """
        Verify that a list exists and the user has access to it.

        Args:
            list_id: The ID of the list to validate

        Returns:
            True if the list exists and is accessible

        Raises:
            ValidationError: If the list ID format is invalid
            ResourceNotFoundError: If the list doesn't exist
            ForbiddenError: If the user doesn't have access
        """
        self.validate_id_format(list_id, "List")

        try:
            logger.debug(f"Validating list exists: {list_id}")
            await self.client.GET(f"/lists/{list_id}", params={"fields": "id"})
            logger.debug(f"List {list_id} exists and is accessible")
            return True
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ResourceNotFoundError("List", list_id)
            elif e.response.status_code == 403:
                raise ForbiddenError("List", list_id, "access")
            raise

    async def validate_card_exists(self, card_id: str) -> bool:
        """
        Verify that a card exists and the user has access to it.

        Args:
            card_id: The ID of the card to validate

        Returns:
            True if the card exists and is accessible

        Raises:
            ValidationError: If the card ID format is invalid
            ResourceNotFoundError: If the card doesn't exist
            ForbiddenError: If the user doesn't have access
        """
        self.validate_id_format(card_id, "Card")

        try:
            logger.debug(f"Validating card exists: {card_id}")
            await self.client.GET(f"/cards/{card_id}", params={"fields": "id"})
            logger.debug(f"Card {card_id} exists and is accessible")
            return True
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ResourceNotFoundError("Card", card_id)
            elif e.response.status_code == 403:
                raise ForbiddenError("Card", card_id, "access")
            raise

    async def validate_organization_exists(self, org_id: str) -> bool:
        """
        Verify that an organization/workspace exists and the user has access to it.

        Args:
            org_id: The ID of the organization to validate

        Returns:
            True if the organization exists and is accessible

        Raises:
            ValidationError: If the organization ID format is invalid
            ResourceNotFoundError: If the organization doesn't exist
            ForbiddenError: If the user doesn't have access
        """
        self.validate_id_format(org_id, "Organization")

        try:
            logger.debug(f"Validating organization exists: {org_id}")
            await self.client.GET(f"/organizations/{org_id}", params={"fields": "id"})
            logger.debug(f"Organization {org_id} exists and is accessible")
            return True
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ResourceNotFoundError("Organization", org_id)
            elif e.response.status_code == 403:
                raise ForbiddenError("Organization", org_id, "access")
            raise

    async def validate_checklist_exists(self, checklist_id: str) -> bool:
        """
        Verify that a checklist exists and the user has access to it.

        Args:
            checklist_id: The ID of the checklist to validate

        Returns:
            True if the checklist exists and is accessible

        Raises:
            ValidationError: If the checklist ID format is invalid
            ResourceNotFoundError: If the checklist doesn't exist
            ForbiddenError: If the user doesn't have access
        """
        self.validate_id_format(checklist_id, "Checklist")

        try:
            logger.debug(f"Validating checklist exists: {checklist_id}")
            await self.client.GET(f"/checklists/{checklist_id}", params={"fields": "id"})
            logger.debug(f"Checklist {checklist_id} exists and is accessible")
            return True
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ResourceNotFoundError("Checklist", checklist_id)
            elif e.response.status_code == 403:
                raise ForbiddenError("Checklist", checklist_id, "access")
            raise

    async def validate_board_admin_permission(
        self, board_id: str, member_id: str = "me"
    ) -> bool:
        """
        Verify that the user has admin permission on a board.

        Args:
            board_id: The ID of the board
            member_id: The ID of the member to check (defaults to "me")

        Returns:
            True if the user has admin permission

        Raises:
            ForbiddenError: If the user doesn't have admin permission
        """
        try:
            logger.debug(f"Validating admin permission for board: {board_id}")
            response = await self.client.GET(
                f"/boards/{board_id}/memberships",
                params={"member": "true", "member_fields": "id"},
            )

            # Check if the current user is an admin
            for membership in response:
                member_type = membership.get("memberType")
                if member_type == "admin":
                    logger.debug(f"User has admin permission on board {board_id}")
                    return True

            raise ForbiddenError("Board", board_id, "modify (admin permission required)")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ResourceNotFoundError("Board", board_id)
            elif e.response.status_code == 403:
                raise ForbiddenError("Board", board_id, "access")
            raise

    async def validate_organization_membership(
        self, org_id: str, member_id: str = "me"
    ) -> bool:
        """
        Verify that the user is a member of an organization.

        Args:
            org_id: The ID of the organization
            member_id: The ID of the member to check (defaults to "me")

        Returns:
            True if the user is a member

        Raises:
            ForbiddenError: If the user is not a member
        """
        try:
            logger.debug(f"Validating membership in organization: {org_id}")
            await self.client.GET(
                f"/organizations/{org_id}/members/{member_id}", params={"fields": "id"}
            )
            logger.debug(f"User is a member of organization {org_id}")
            return True
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ForbiddenError(
                    "Organization",
                    org_id,
                    "access (membership required)",
                )
            elif e.response.status_code == 403:
                raise ForbiddenError("Organization", org_id, "access")
            raise

    def validate_permission_level(self, level: str) -> None:
        """
        Validate that a permission level is valid.

        Args:
            level: The permission level to validate

        Raises:
            ValidationError: If the permission level is invalid
        """
        valid_levels = ["private", "org", "public"]
        if level not in valid_levels:
            raise ValidationError(
                f"Invalid permission level '{level}'. Must be one of: {', '.join(valid_levels)}"
            )

    def validate_comments_permission(self, permission: str) -> None:
        """
        Validate that a comments permission value is valid.

        Args:
            permission: The comments permission to validate

        Raises:
            ValidationError: If the permission is invalid
        """
        valid_permissions = ["disabled", "members", "observers", "org", "public"]
        if permission not in valid_permissions:
            raise ValidationError(
                f"Invalid comments permission '{permission}'. Must be one of: {', '.join(valid_permissions)}"
            )

    def validate_voting_permission(self, permission: str) -> None:
        """
        Validate that a voting permission value is valid.

        Args:
            permission: The voting permission to validate

        Raises:
            ValidationError: If the permission is invalid
        """
        valid_permissions = ["disabled", "members", "observers", "org", "public"]
        if permission not in valid_permissions:
            raise ValidationError(
                f"Invalid voting permission '{permission}'. Must be one of: {', '.join(valid_permissions)}"
            )

    def validate_board_filter(self, filter_value: str) -> None:
        """
        Validate that a board filter value is valid.

        Args:
            filter_value: The filter value to validate

        Raises:
            ValidationError: If the filter value is invalid
        """
        valid_filters = ["all", "open", "closed", "members", "organization", "public"]
        if filter_value not in valid_filters:
            raise ValidationError(
                f"Invalid board filter '{filter_value}'. Must be one of: {', '.join(valid_filters)}"
            )

    def validate_url(self, url: str, field_name: str = "URL") -> None:
        """
        Validate that a URL is properly formatted.

        Args:
            url: The URL to validate
            field_name: Name of the field (for error messages)

        Raises:
            ValidationError: If the URL is invalid
        """
        url_pattern = re.compile(
            r"^https?://"
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"
            r"localhost|"
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            r"(?::\d+)?"
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

        if not url_pattern.match(url):
            raise ValidationError(
                f"Invalid {field_name} format. Must be a valid HTTP or HTTPS URL."
            )

    def validate_color(self, color: str) -> None:
        """
        Validate that a color value is valid for Trello labels.

        Args:
            color: The color to validate

        Raises:
            ValidationError: If the color is invalid
        """
        valid_colors = [
            "yellow",
            "purple",
            "blue",
            "red",
            "green",
            "orange",
            "black",
            "sky",
            "pink",
            "lime",
            None,
        ]
        if color not in valid_colors:
            raise ValidationError(
                f"Invalid color '{color}'. Must be one of: {', '.join(str(c) for c in valid_colors if c)}, or null"
            )
