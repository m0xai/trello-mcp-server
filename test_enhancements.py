"""
Test script for Trello MCP Server enhancements.
Validates imports, models, and basic functionality.
"""

import sys
import os
import asyncio
from typing import Optional

# Set dummy environment variables for testing
os.environ["TRELLO_API_KEY"] = "test_api_key_for_testing_only"
os.environ["TRELLO_TOKEN"] = "test_token_for_testing_only"


def test_imports():
    """Test that all new modules can be imported."""
    print("Testing imports...")
    
    try:
        from server.exceptions import (
            TrelloMCPError,
            ValidationError,
            ResourceNotFoundError,
            UnauthorizedError,
            ForbiddenError,
            RateLimitError,
            ConflictError,
            BadRequestError,
        )
        print("✓ Exceptions imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import exceptions: {e}")
        return False
    
    try:
        from server.validators import ValidationService
        print("✓ ValidationService imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import ValidationService: {e}")
        return False
    
    try:
        from server.dtos.create_board import CreateBoardPayload
        from server.dtos.update_board import UpdateBoardPayload
        from server.dtos.update_workspace import UpdateWorkspacePayload
        print("✓ DTOs imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import DTOs: {e}")
        return False
    
    try:
        from server.models import TrelloBoard, TrelloOrganization
        print("✓ Models imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import models: {e}")
        return False
    
    try:
        from server.services.board import BoardService
        from server.services.workspace import WorkspaceService
        print("✓ Services imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import services: {e}")
        return False
    
    try:
        from server.tools import board, workspace
        print("✓ Tools imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import tools: {e}")
        return False
    
    return True


def test_exception_hierarchy():
    """Test exception hierarchy and messages."""
    print("\nTesting exception hierarchy...")
    
    from server.exceptions import (
        TrelloMCPError,
        ValidationError,
        ResourceNotFoundError,
        ForbiddenError,
    )
    
    # Test base exception
    base_error = TrelloMCPError("Test error", status_code=500)
    assert base_error.message == "Test error"
    assert base_error.status_code == 500
    print("✓ Base exception works correctly")
    
    # Test ValidationError
    validation_error = ValidationError("Invalid input")
    assert validation_error.status_code == 400
    print("✓ ValidationError has correct status code")
    
    # Test ResourceNotFoundError
    not_found_error = ResourceNotFoundError("Board", "123abc")
    assert "Board" in not_found_error.message
    assert "123abc" in not_found_error.message
    assert not_found_error.status_code == 404
    print("✓ ResourceNotFoundError formats message correctly")
    
    # Test ForbiddenError
    forbidden_error = ForbiddenError("Board", "456def", "modify")
    assert "Board" in forbidden_error.message
    assert "456def" in forbidden_error.message
    assert "modify" in forbidden_error.message
    assert forbidden_error.status_code == 403
    print("✓ ForbiddenError formats message correctly")
    
    return True


def test_dto_validation():
    """Test DTO validation with Pydantic."""
    print("\nTesting DTO validation...")
    
    from server.dtos.create_board import CreateBoardPayload
    from server.dtos.update_board import UpdateBoardPayload
    from server.dtos.update_workspace import UpdateWorkspacePayload
    from pydantic import ValidationError as PydanticValidationError
    
    # Test CreateBoardPayload - valid
    try:
        payload = CreateBoardPayload(
            name="Test Board",
            desc="Test description",
            prefs_permission_level="private"
        )
        assert payload.name == "Test Board"
        assert payload.prefs_permission_level == "private"
        print("✓ CreateBoardPayload accepts valid input")
    except Exception as e:
        print(f"✗ CreateBoardPayload failed with valid input: {e}")
        return False
    
    # Test CreateBoardPayload - invalid permission level
    try:
        payload = CreateBoardPayload(
            name="Test Board",
            prefs_permission_level="invalid"
        )
        print("✗ CreateBoardPayload should reject invalid permission level")
        return False
    except PydanticValidationError:
        print("✓ CreateBoardPayload rejects invalid permission level")
    
    # Test UpdateBoardPayload - valid
    try:
        payload = UpdateBoardPayload(
            name="Updated Board",
            closed=True
        )
        params = payload.to_api_params()
        assert params["name"] == "Updated Board"
        assert params["closed"] == True
        print("✓ UpdateBoardPayload converts to API params correctly")
    except Exception as e:
        print(f"✗ UpdateBoardPayload failed: {e}")
        return False
    
    # Test UpdateWorkspacePayload - valid URL
    try:
        payload = UpdateWorkspacePayload(
            display_name="Test Workspace",
            website="https://example.com"
        )
        assert payload.website == "https://example.com"
        print("✓ UpdateWorkspacePayload accepts valid URL")
    except Exception as e:
        print(f"✗ UpdateWorkspacePayload failed with valid URL: {e}")
        return False
    
    # Test UpdateWorkspacePayload - invalid URL
    try:
        payload = UpdateWorkspacePayload(
            display_name="Test Workspace",
            website="not-a-url"
        )
        print("✗ UpdateWorkspacePayload should reject invalid URL")
        return False
    except PydanticValidationError:
        print("✓ UpdateWorkspacePayload rejects invalid URL")
    
    return True


def test_validation_service():
    """Test ValidationService methods (without actual API calls)."""
    print("\nTesting ValidationService...")
    
    from server.validators.validation_service import ValidationService
    from server.exceptions import ValidationError
    
    # Create a mock client (we won't actually call API)
    class MockClient:
        pass
    
    validator = ValidationService(MockClient())
    
    # Test ID format validation - valid
    try:
        validator.validate_id_format("507f1f77bcf86cd799439011", "Board")
        print("✓ Accepts valid 24-char hex ID")
    except ValidationError:
        print("✗ Should accept valid ID format")
        return False
    
    # Test ID format validation - invalid (too short)
    try:
        validator.validate_id_format("123", "Board")
        print("✗ Should reject short ID")
        return False
    except ValidationError:
        print("✓ Rejects short ID")
    
    # Test ID format validation - invalid (non-hex)
    try:
        validator.validate_id_format("gggggggggggggggggggggggg", "Board")
        print("✗ Should reject non-hex ID")
        return False
    except ValidationError:
        print("✓ Rejects non-hex ID")
    
    # Test permission level validation - valid
    try:
        validator.validate_permission_level("private")
        validator.validate_permission_level("org")
        validator.validate_permission_level("public")
        print("✓ Accepts valid permission levels")
    except ValidationError:
        print("✗ Should accept valid permission levels")
        return False
    
    # Test permission level validation - invalid
    try:
        validator.validate_permission_level("invalid")
        print("✗ Should reject invalid permission level")
        return False
    except ValidationError:
        print("✓ Rejects invalid permission level")
    
    # Test color validation - valid
    try:
        validator.validate_color("red")
        validator.validate_color("blue")
        validator.validate_color(None)
        print("✓ Accepts valid colors")
    except ValidationError:
        print("✗ Should accept valid colors")
        return False
    
    # Test color validation - invalid
    try:
        validator.validate_color("invalid")
        print("✗ Should reject invalid color")
        return False
    except ValidationError:
        print("✓ Rejects invalid color")
    
    return True


def test_models():
    """Test Pydantic models."""
    print("\nTesting models...")
    
    from server.models import TrelloBoard, TrelloOrganization
    
    # Test TrelloBoard
    try:
        board = TrelloBoard(
            id="507f1f77bcf86cd799439011",
            name="Test Board",
            url="https://trello.com/b/test",
            desc="Test description",
            closed=False
        )
        assert board.name == "Test Board"
        assert board.closed == False
        print("✓ TrelloBoard model works correctly")
    except Exception as e:
        print(f"✗ TrelloBoard model failed: {e}")
        return False
    
    # Test TrelloOrganization
    try:
        org = TrelloOrganization(
            id="507f1f77bcf86cd799439011",
            name="test_org",
            displayName="Test Organization",
            url="https://trello.com/w/test_org",
            desc="Test workspace"
        )
        assert org.displayName == "Test Organization"
        assert org.name == "test_org"
        print("✓ TrelloOrganization model works correctly")
    except Exception as e:
        print(f"✗ TrelloOrganization model failed: {e}")
        return False
    
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Trello MCP Server Enhancement Tests")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Exception Hierarchy", test_exception_hierarchy),
        ("DTO Validation", test_dto_validation),
        ("Validation Service", test_validation_service),
        ("Models", test_models),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
