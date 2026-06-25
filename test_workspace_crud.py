"""
Test script for Trello MCP Server workspace CRUD operations.
"""

import sys
import os

# Set dummy environment variables for testing
os.environ["TRELLO_API_KEY"] = "test_api_key_for_testing_only"
os.environ["TRELLO_TOKEN"] = "test_token_for_testing_only"


def test_workspace_imports():
    """Test that workspace CRUD modules can be imported."""
    print("Testing workspace CRUD imports...")
    
    try:
        from server.dtos.create_workspace import CreateWorkspacePayload
        print("✓ CreateWorkspacePayload imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import CreateWorkspacePayload: {e}")
        return False
    
    try:
        from server.services.workspace import WorkspaceService
        print("✓ WorkspaceService imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import WorkspaceService: {e}")
        return False
    
    try:
        from server.tools import workspace
        # Check that new functions exist
        assert hasattr(workspace, 'create_workspace')
        assert hasattr(workspace, 'delete_workspace')
        print("✓ Workspace tools (create, delete) imported successfully")
    except (ImportError, AssertionError) as e:
        print(f"✗ Failed to import workspace tools: {e}")
        return False
    
    return True


def test_create_workspace_payload():
    """Test CreateWorkspacePayload validation."""
    print("\nTesting CreateWorkspacePayload validation...")
    
    from server.dtos.create_workspace import CreateWorkspacePayload
    from pydantic import ValidationError as PydanticValidationError
    
    # Test valid payload
    try:
        payload = CreateWorkspacePayload(
            display_name="Test Workspace",
            desc="Test description",
            name="test_workspace",
            website="https://example.com"
        )
        assert payload.display_name == "Test Workspace"
        assert payload.name == "test_workspace"
        print("✓ CreateWorkspacePayload accepts valid input")
    except Exception as e:
        print(f"✗ CreateWorkspacePayload failed with valid input: {e}")
        return False
    
    # Test missing required field (display_name)
    try:
        payload = CreateWorkspacePayload(
            desc="Test description"
        )
        print("✗ CreateWorkspacePayload should require display_name")
        return False
    except PydanticValidationError:
        print("✓ CreateWorkspacePayload requires display_name")
    
    # Test invalid workspace name (uppercase)
    try:
        payload = CreateWorkspacePayload(
            display_name="Test Workspace",
            name="TestWorkspace"  # Should be lowercase
        )
        print("✗ CreateWorkspacePayload should reject uppercase in name")
        return False
    except PydanticValidationError:
        print("✓ CreateWorkspacePayload rejects invalid name format")
    
    # Test invalid workspace name (too short)
    try:
        payload = CreateWorkspacePayload(
            display_name="Test Workspace",
            name="ab"  # Should be at least 3 chars
        )
        print("✗ CreateWorkspacePayload should reject short names")
        return False
    except PydanticValidationError:
        print("✓ CreateWorkspacePayload rejects short names")
    
    # Test invalid URL
    try:
        payload = CreateWorkspacePayload(
            display_name="Test Workspace",
            website="not-a-url"
        )
        print("✗ CreateWorkspacePayload should reject invalid URL")
        return False
    except PydanticValidationError:
        print("✓ CreateWorkspacePayload rejects invalid URL")
    
    # Test to_api_params conversion
    try:
        payload = CreateWorkspacePayload(
            display_name="Test Workspace",
            desc="Test description",
            name="test_workspace"
        )
        params = payload.to_api_params()
        assert params["displayName"] == "Test Workspace"
        assert params["desc"] == "Test description"
        assert params["name"] == "test_workspace"
        assert "website" not in params  # Should not include None values
        print("✓ CreateWorkspacePayload converts to API params correctly")
    except Exception as e:
        print(f"✗ CreateWorkspacePayload to_api_params failed: {e}")
        return False
    
    return True


def test_workspace_service_methods():
    """Test that WorkspaceService has create and delete methods."""
    print("\nTesting WorkspaceService methods...")
    
    from server.services.workspace import WorkspaceService
    
    # Create a mock client
    class MockClient:
        pass
    
    service = WorkspaceService(MockClient())
    
    # Check methods exist
    try:
        assert hasattr(service, 'create_workspace')
        assert hasattr(service, 'delete_workspace')
        assert hasattr(service, 'get_workspaces')
        assert hasattr(service, 'get_workspace')
        assert hasattr(service, 'get_workspace_boards')
        assert hasattr(service, 'update_workspace')
        print("✓ WorkspaceService has all CRUD methods")
    except AssertionError:
        print("✗ WorkspaceService missing methods")
        return False
    
    # Check method signatures
    import inspect
    
    create_sig = inspect.signature(service.create_workspace)
    assert 'kwargs' in str(create_sig)
    print("✓ create_workspace has correct signature")
    
    delete_sig = inspect.signature(service.delete_workspace)
    assert 'workspace_id' in str(delete_sig)
    print("✓ delete_workspace has correct signature")
    
    return True


def test_workspace_tools():
    """Test that workspace tools are properly defined."""
    print("\nTesting workspace tools...")
    
    from server.tools import workspace
    import inspect
    
    # Check create_workspace tool
    try:
        assert hasattr(workspace, 'create_workspace')
        sig = inspect.signature(workspace.create_workspace)
        params = list(sig.parameters.keys())
        assert 'ctx' in params
        assert 'payload' in params
        print("✓ create_workspace tool has correct signature")
    except AssertionError as e:
        print(f"✗ create_workspace tool signature incorrect: {e}")
        return False
    
    # Check delete_workspace tool
    try:
        assert hasattr(workspace, 'delete_workspace')
        sig = inspect.signature(workspace.delete_workspace)
        params = list(sig.parameters.keys())
        assert 'ctx' in params
        assert 'workspace_id' in params
        print("✓ delete_workspace tool has correct signature")
    except AssertionError as e:
        print(f"✗ delete_workspace tool signature incorrect: {e}")
        return False
    
    # Check all workspace tools
    expected_tools = [
        'get_workspaces',
        'get_workspace',
        'get_workspace_boards',
        'create_workspace',
        'update_workspace',
        'delete_workspace'
    ]
    
    for tool_name in expected_tools:
        if not hasattr(workspace, tool_name):
            print(f"✗ Missing tool: {tool_name}")
            return False
    
    print(f"✓ All {len(expected_tools)} workspace tools present")
    
    return True


def test_tools_registration():
    """Test that workspace CRUD tools are registered."""
    print("\nTesting tools registration...")
    
    from server.tools import tools
    import inspect
    
    # Get the register_tools function source
    source = inspect.getsource(tools.register_tools)
    
    # Check that create and delete are registered
    if 'workspace.create_workspace' in source:
        print("✓ create_workspace is registered")
    else:
        print("✗ create_workspace not registered")
        return False
    
    if 'workspace.delete_workspace' in source:
        print("✓ delete_workspace is registered")
    else:
        print("✗ delete_workspace not registered")
        return False
    
    return True


def main():
    """Run all workspace CRUD tests."""
    print("=" * 60)
    print("Trello MCP Server Workspace CRUD Tests")
    print("=" * 60)
    
    tests = [
        ("Workspace CRUD Imports", test_workspace_imports),
        ("CreateWorkspacePayload Validation", test_create_workspace_payload),
        ("WorkspaceService Methods", test_workspace_service_methods),
        ("Workspace Tools", test_workspace_tools),
        ("Tools Registration", test_tools_registration),
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
        print("\n🎉 All workspace CRUD tests passed!")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
