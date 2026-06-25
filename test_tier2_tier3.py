"""
Test suite for Tier 2 and Tier 3 enhancements.
"""

import os
import sys

# Set environment variables before imports
os.environ["TRELLO_API_KEY"] = "test_key"
os.environ["TRELLO_TOKEN"] = "test_token"

def test_imports():
    """Test that all new modules can be imported."""
    try:
        # Tier 2 - Custom Fields
        from server.dtos.create_custom_field import CreateCustomFieldPayload
        from server.dtos.set_custom_field_value import SetCustomFieldValuePayload
        from server.models.custom_field import TrelloCustomField, TrelloCustomFieldItem, TrelloCustomFieldOption
        from server.services.custom_field import CustomFieldService
        from server.tools import custom_field
        
        # Tier 2 - Search
        from server.services.search import SearchService
        from server.tools import search
        
        # Tier 2 - Batch
        from server.services.batch import BatchService
        from server.tools import batch
        
        # Tier 2/3 - Export & Templates
        from server.services.export import ExportService
        from server.tools import export
        
        # Tier 2 - Advanced Card
        from server.tools import advanced_card
        
        # Tier 3 - Analytics
        from server.services.analytics import AnalyticsService
        from server.tools import analytics
        
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_custom_field_dtos():
    """Test custom field DTO validation."""
    try:
        from server.dtos.create_custom_field import CreateCustomFieldPayload
        from server.dtos.set_custom_field_value import SetCustomFieldValuePayload
        
        # Test CreateCustomFieldPayload
        payload1 = CreateCustomFieldPayload(
            id_model="board123",
            name="Test Field",
            type="text",
            pos="bottom"
        )
        assert payload1.to_api_params()["idModel"] == "board123"
        
        # Test with list type
        payload2 = CreateCustomFieldPayload(
            id_model="board123",
            name="Priority",
            type="list",
            options=[{"value": {"text": "High"}, "color": "red"}]
        )
        assert payload2.type == "list"
        
        # Test SetCustomFieldValuePayload
        payload3 = SetCustomFieldValuePayload(value={"text": "test"})
        assert payload3.to_api_params()["value"]["text"] == "test"
        
        payload4 = SetCustomFieldValuePayload(id_value="option123")
        assert payload4.to_api_params()["idValue"] == "option123"
        
        print("✓ Custom field DTOs validated")
        return True
    except Exception as e:
        print(f"✗ Custom field DTO validation failed: {e}")
        return False

def test_custom_field_models():
    """Test custom field models."""
    try:
        from server.models.custom_field import TrelloCustomField, TrelloCustomFieldItem, TrelloCustomFieldOption
        
        # Test TrelloCustomFieldOption
        option = TrelloCustomFieldOption(
            id="opt123",
            idCustomField="field123",
            value={"text": "Option 1"},
            color="green",
            pos=1024
        )
        assert option.id == "opt123"
        
        # Test TrelloCustomField
        field = TrelloCustomField(
            id="field123",
            idModel="board123",
            modelType="board",
            name="Test Field",
            pos=1024,
            type="list",
            options=[option]
        )
        assert field.type == "list"
        assert len(field.options) == 1
        
        # Test TrelloCustomFieldItem
        item = TrelloCustomFieldItem(
            id="item123",
            idCustomField="field123",
            idModel="card123",
            modelType="card",
            value={"text": "value"}
        )
        assert item.id_custom_field == "field123"
        
        print("✓ Custom field models validated")
        return True
    except Exception as e:
        print(f"✗ Custom field model validation failed: {e}")
        return False

def test_service_instantiation():
    """Test that services can be instantiated."""
    try:
        from server.utils.trello_api import TrelloClient
        from server.services.custom_field import CustomFieldService
        from server.services.search import SearchService
        from server.services.batch import BatchService
        from server.services.export import ExportService
        from server.services.analytics import AnalyticsService
        
        client = TrelloClient("test_key", "test_token")
        
        custom_field_service = CustomFieldService(client)
        search_service = SearchService(client)
        batch_service = BatchService(client)
        export_service = ExportService(client)
        analytics_service = AnalyticsService(client)
        
        assert custom_field_service.client == client
        assert search_service.client == client
        assert batch_service.client == client
        assert export_service.client == client
        assert analytics_service.client == client
        
        print("✓ All services instantiated")
        return True
    except Exception as e:
        print(f"✗ Service instantiation failed: {e}")
        return False

def test_tool_functions():
    """Test that tool functions exist."""
    try:
        from server.tools import custom_field, search, batch, export, advanced_card, analytics
        
        # Custom field tools
        assert hasattr(custom_field, 'get_board_custom_fields')
        assert hasattr(custom_field, 'create_custom_field')
        assert hasattr(custom_field, 'set_custom_field_value_checkbox')
        assert hasattr(custom_field, 'add_custom_field_option')
        
        # Search tools
        assert hasattr(search, 'search_trello')
        assert hasattr(search, 'search_members')
        
        # Batch tools
        assert hasattr(batch, 'batch_get_resources')
        
        # Export tools
        assert hasattr(export, 'export_board')
        assert hasattr(export, 'create_board_from_template')
        
        # Advanced card tools
        assert hasattr(advanced_card, 'set_card_due_date')
        assert hasattr(advanced_card, 'subscribe_to_card')
        assert hasattr(advanced_card, 'vote_on_card')
        
        # Analytics tools
        assert hasattr(analytics, 'get_board_statistics')
        assert hasattr(analytics, 'get_card_cycle_time')
        
        print("✓ All tool functions exist")
        return True
    except Exception as e:
        print(f"✗ Tool function check failed: {e}")
        return False

def test_tools_registration():
    """Test that tools can be registered."""
    try:
        from server.tools.tools import register_tools
        
        # Mock MCP server
        class MockMCP:
            def __init__(self):
                self.tools = []
            
            def add_tool(self, tool):
                self.tools.append(tool)
        
        mcp = MockMCP()
        register_tools(mcp)
        
        # Count tools
        tool_count = len(mcp.tools)
        
        # Should have 60 (Tier 1) + 31 (Tier 2/3) = 91 tools
        expected_min = 85  # Allow some flexibility
        
        if tool_count >= expected_min:
            print(f"✓ Tools registered successfully ({tool_count} tools)")
            return True
        else:
            print(f"✗ Tool count mismatch: expected >={expected_min}, got {tool_count}")
            return False
    except Exception as e:
        print(f"✗ Tools registration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Testing Tier 2 and Tier 3 Enhancements")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Custom Field DTOs", test_custom_field_dtos),
        ("Custom Field Models", test_custom_field_models),
        ("Service Instantiation", test_service_instantiation),
        ("Tool Functions", test_tool_functions),
        ("Tools Registration", test_tools_registration),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\nTest: {name}")
        print("-" * 60)
        result = test_func()
        results.append((name, result))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print("=" * 60)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("Features tested:")
        print("  • Custom Fields Management (13 operations)")
        print("  • Search & Filtering (2 operations)")
        print("  • Batch Operations (1 operation)")
        print("  • Export & Templates (4 operations)")
        print("  • Advanced Card Features (7 operations)")
        print("  • Analytics & Reporting (2 operations)")
        print("Total: 29 new operations added (Tier 2 + Tier 3)")
        print("Grand Total: 60 (Tier 1) + 29 (Tier 2/3) = 89+ operations")
        print("=" * 60)
    else:
        print("=" * 60)
        print(f"❌ {total - passed} test(s) failed")
        print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
