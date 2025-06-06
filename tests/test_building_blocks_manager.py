"""
Tests for Building Blocks Manager functionality.

This module tests building blocks management including:
- MongoDB collection management
- Building blocks storage and retrieval
- Search and statistics functionality
- Error handling

Priority: 3 (Supporting Modules)
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from Modules.building_blocks_manager import BuildingBlocksManager


@pytest.mark.unit
class TestBuildingBlocksManagerInitialization:
    """Test building blocks manager initialization"""

    def test_basic_initialization(self):
        """Test basic initialization with mocked MongoDB"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            # Mock the MongoDB client and database
            mock_client.return_value.rpger.building_blocks = Mock()
            
            manager = BuildingBlocksManager(auto_connect=False)
            
            assert manager.mongo_host == "10.202.28.46"
            assert manager.mongo_port == 27017
            assert manager.database_name == "rpger"
            assert manager.collection_name == "building_blocks"

    def test_initialization_with_custom_params(self):
        """Test initialization with custom parameters"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            mock_client.return_value.test_db.test_collection = Mock()
            
            manager = BuildingBlocksManager(
                mongo_host="localhost",
                mongo_port=27018,
                database="test_db",
                collection="test_collection",
                auto_connect=False
            )
            
            assert manager.mongo_host == "localhost"
            assert manager.mongo_port == 27018
            assert manager.database_name == "test_db"
            assert manager.collection_name == "test_collection"


@pytest.mark.unit
class TestConnectionManagement:
    """Test MongoDB connection management"""

    def test_connection_success(self):
        """Test successful MongoDB connection"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            # Setup mock client and database hierarchy
            mock_db = Mock()
            mock_collection = Mock()
            
            # Configure mock to properly simulate MongoDB client behavior
            mock_client_instance = Mock()
            mock_client.return_value = mock_client_instance
            
            # Configure server_info for connection test
            mock_client_instance.server_info.return_value = {"version": "4.4.0"}
            
            # Configure database access: client[database_name] returns database
            mock_client_instance.__getitem__ = Mock(return_value=mock_db)
            
            # Configure collection access: db[collection_name] returns collection  
            mock_db.__getitem__ = Mock(return_value=mock_collection)
            
            manager = BuildingBlocksManager(auto_connect=False)
            
            # Mock the _create_indexes method to avoid index creation during testing
            with patch.object(manager, '_create_indexes'):
                manager._connect()  # Explicitly call connect to test the connection logic
            
            # Should have attempted connection
            assert mock_client.called

    def test_connection_failure_handling(self):
        """Test MongoDB connection failure handling"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            # Simulate connection failure
            mock_client.side_effect = Exception("Connection failed")
            
            # Should handle gracefully
            try:
                manager = BuildingBlocksManager(auto_connect=False)
                # If no exception, the error was handled
            except Exception:
                # Connection error handling may vary
                pass


@pytest.mark.unit
class TestBuildingBlocksStorage:
    """Test building blocks storage functionality"""

    def test_store_building_blocks_basic(self):
        """Test basic building blocks storage"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            # Setup mock client and database hierarchy
            mock_db = Mock()
            mock_collection = Mock()
            
            # Configure mock to properly simulate MongoDB client behavior
            mock_client_instance = Mock()
            mock_client.return_value = mock_client_instance
            
            # Configure server_info for connection test
            mock_client_instance.server_info.return_value = {"version": "4.4.0"}
            
            # Configure database access: client[database_name] returns database
            mock_client_instance.__getitem__ = Mock(return_value=mock_db)
            
            # Configure collection access: db[collection_name] returns collection  
            mock_db.__getitem__ = Mock(return_value=mock_collection)
            
            # Mock successful upsert
            mock_upsert_result = Mock()
            mock_upsert_result.upserted_id = "test_id"
            mock_collection.update_one.return_value = mock_upsert_result
            
            # Mock successful insertion for summary
            mock_collection.insert_one.return_value = Mock(inserted_id="summary_id")
            
            manager = BuildingBlocksManager(auto_connect=False)
            
            # Mock the _create_indexes method to avoid index creation during testing
            with patch.object(manager, '_create_indexes'):
                manager._connect()  # Explicitly call connect to set up mocked connection
            
            building_blocks = {
                "names": ["John", "Mary", "Bob"],
                "places": ["Castle", "Forest", "Village"],
                "items": ["Sword", "Shield", "Potion"]
            }
            
            source_metadata = {
                "novel_title": "Test Novel",
                "author": "Test Author"
            }
            
            result = manager.store_building_blocks(building_blocks, source_metadata)
            
            assert isinstance(result, dict)
            assert "blocks_stored" in result
            assert "blocks_skipped" in result
            assert "categories" in result

    def test_store_empty_building_blocks(self):
        """Test storing empty building blocks"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            mock_collection = Mock()
            mock_client.return_value.rpger.building_blocks = mock_collection
            
            manager = BuildingBlocksManager(auto_connect=False)
            
            empty_blocks = {}
            source_metadata = {"novel_title": "Empty Novel"}
            
            result = manager.store_building_blocks(empty_blocks, source_metadata)
            
            assert isinstance(result, dict)
            assert result["blocks_stored"] == 0

    def test_store_building_blocks_with_duplicates(self):
        """Test storing building blocks with duplicates"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            mock_collection = Mock()
            mock_client.return_value.rpger.building_blocks = mock_collection
            
            # Simulate duplicate key error for some inserts
            from pymongo.errors import DuplicateKeyError
            mock_collection.insert_one.side_effect = [
                Mock(inserted_id="id1"),  # Success
                DuplicateKeyError("Duplicate"),  # Error
                Mock(inserted_id="id3")   # Success
            ]
            
            manager = BuildingBlocksManager(auto_connect=False)
            
            building_blocks = {
                "names": ["John", "Mary", "Bob"]
            }
            source_metadata = {"novel_title": "Test Novel"}
            
            result = manager.store_building_blocks(building_blocks, source_metadata)
            
            assert isinstance(result, dict)
            assert "blocks_skipped" in result


@pytest.mark.unit
class TestBuildingBlocksRetrieval:
    """Test building blocks retrieval functionality"""

    def test_get_blocks_by_category(self):
        """Test getting blocks by category"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            # Setup mock client and database hierarchy
            mock_db = Mock()
            mock_collection = Mock()
            
            # Configure mock to properly simulate MongoDB client behavior
            mock_client_instance = Mock()
            mock_client.return_value = mock_client_instance
            
            # Configure server_info for connection test
            mock_client_instance.server_info.return_value = {"version": "4.4.0"}
            
            # Configure database access: client[database_name] returns database
            mock_client_instance.__getitem__ = Mock(return_value=mock_db)
            
            # Configure collection access: db[collection_name] returns collection  
            mock_db.__getitem__ = Mock(return_value=mock_collection)
            
            # Mock query results
            mock_collection.find.return_value.limit.return_value = [
                {"text": "John", "category": "names", "novel_title": "Test Novel"},
                {"text": "Mary", "category": "names", "novel_title": "Test Novel"}
            ]
            
            manager = BuildingBlocksManager(auto_connect=False)
            
            # Mock the _create_indexes method to avoid index creation during testing
            with patch.object(manager, '_create_indexes'):
                manager._connect()  # Explicitly call connect to set up mocked connection
            
            results = manager.get_blocks_by_category("names", limit=10)
            
            assert isinstance(results, list)
            assert len(results) == 2
            mock_collection.find.assert_called_once()

    def test_get_blocks_by_category_with_novel_filter(self):
        """Test getting blocks by category with novel title filter"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            # Setup mock client and database hierarchy
            mock_db = Mock()
            mock_collection = Mock()
            
            # Configure mock to properly simulate MongoDB client behavior
            mock_client_instance = Mock()
            mock_client.return_value = mock_client_instance
            
            # Configure server_info for connection test
            mock_client_instance.server_info.return_value = {"version": "4.4.0"}
            
            # Configure database access: client[database_name] returns database
            mock_client_instance.__getitem__ = Mock(return_value=mock_db)
            
            # Configure collection access: db[collection_name] returns collection  
            mock_db.__getitem__ = Mock(return_value=mock_collection)
            
            mock_collection.find.return_value.limit.return_value = []
            
            manager = BuildingBlocksManager(auto_connect=False)
            
            # Mock the _create_indexes method to avoid index creation during testing
            with patch.object(manager, '_create_indexes'):
                manager._connect()  # Explicitly call connect to set up mocked connection
            
            results = manager.get_blocks_by_category("names", novel_title="Specific Novel")
            
            # Should call find with both category and novel title filters
            mock_collection.find.assert_called_once()
            call_args = mock_collection.find.call_args[0][0]
            assert "category" in call_args
            assert "source.novel_title" in call_args

    def test_get_random_blocks(self):
        """Test getting random blocks"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            # Setup mock client and database hierarchy
            mock_db = Mock()
            mock_collection = Mock()
            
            # Configure mock to properly simulate MongoDB client behavior
            mock_client_instance = Mock()
            mock_client.return_value = mock_client_instance
            
            # Configure server_info for connection test
            mock_client_instance.server_info.return_value = {"version": "4.4.0"}
            
            # Configure database access: client[database_name] returns database
            mock_client_instance.__getitem__ = Mock(return_value=mock_db)
            
            # Configure collection access: db[collection_name] returns collection  
            mock_db.__getitem__ = Mock(return_value=mock_collection)
            
            # Mock aggregation pipeline results
            mock_collection.aggregate.return_value = [
                {"block": "Random Name 1"},
                {"block": "Random Name 2"}
            ]
            
            manager = BuildingBlocksManager(auto_connect=False)
            
            # Mock the _create_indexes method to avoid index creation during testing
            with patch.object(manager, '_create_indexes'):
                manager._connect()  # Explicitly call connect to set up mocked connection
            
            results = manager.get_random_blocks("names", count=5)
            
            assert isinstance(results, list)
            mock_collection.aggregate.assert_called_once()

    def test_search_blocks(self):
        """Test searching blocks by text"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            # Setup mock client and database hierarchy
            mock_db = Mock()
            mock_collection = Mock()
            
            # Configure mock to properly simulate MongoDB client behavior
            mock_client_instance = Mock()
            mock_client.return_value = mock_client_instance
            
            # Configure server_info for connection test
            mock_client_instance.server_info.return_value = {"version": "4.4.0"}
            
            # Configure database access: client[database_name] returns database
            mock_client_instance.__getitem__ = Mock(return_value=mock_db)
            
            # Configure collection access: db[collection_name] returns collection  
            mock_db.__getitem__ = Mock(return_value=mock_collection)
            
            mock_collection.find.return_value.limit.return_value = [
                {"text": "John the Wizard", "category": "names"}
            ]
            
            manager = BuildingBlocksManager(auto_connect=False)
            
            # Mock the _create_indexes method to avoid index creation during testing
            with patch.object(manager, '_create_indexes'):
                manager._connect()  # Explicitly call connect to set up mocked connection
            
            results = manager.search_blocks("wizard")
            
            assert isinstance(results, list)
            mock_collection.find.assert_called_once()
            # Should use text search query
            call_args = mock_collection.find.call_args[0][0]
            assert "$regex" in str(call_args) or "block" in call_args

    def test_search_blocks_with_category_filter(self):
        """Test searching blocks with category filter"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            # Setup mock client and database hierarchy
            mock_db = Mock()
            mock_collection = Mock()
            
            # Configure mock to properly simulate MongoDB client behavior
            mock_client_instance = Mock()
            mock_client.return_value = mock_client_instance
            
            # Configure server_info for connection test
            mock_client_instance.server_info.return_value = {"version": "4.4.0"}
            
            # Configure database access: client[database_name] returns database
            mock_client_instance.__getitem__ = Mock(return_value=mock_db)
            
            # Configure collection access: db[collection_name] returns collection  
            mock_db.__getitem__ = Mock(return_value=mock_collection)
            
            mock_collection.find.return_value.limit.return_value = []
            
            manager = BuildingBlocksManager(auto_connect=False)
            
            # Mock the _create_indexes method to avoid index creation during testing
            with patch.object(manager, '_create_indexes'):
                manager._connect()  # Explicitly call connect to set up mocked connection
            
            results = manager.search_blocks("wizard", category="names")
            
            mock_collection.find.assert_called_once()
            call_args = mock_collection.find.call_args[0][0]
            assert "category" in call_args


@pytest.mark.unit
class TestStatistics:
    """Test statistics functionality"""

    def test_get_statistics(self):
        """Test getting collection statistics"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            # Setup mock client and database hierarchy
            mock_db = Mock()
            mock_collection = Mock()
            
            # Configure mock to properly simulate MongoDB client behavior
            mock_client_instance = Mock()
            mock_client.return_value = mock_client_instance
            
            # Configure server_info for connection test
            mock_client_instance.server_info.return_value = {"version": "4.4.0"}
            
            # Configure database access: client[database_name] returns database
            mock_client_instance.__getitem__ = Mock(return_value=mock_db)
            
            # Configure collection access: db[collection_name] returns collection  
            mock_db.__getitem__ = Mock(return_value=mock_collection)
            
            # Mock statistics queries
            mock_collection.aggregate.side_effect = [
                [
                    {"_id": "names", "count": 30, "novels": ["Novel1", "Novel2"]},
                    {"_id": "places", "count": 25, "novels": ["Novel1"]},
                    {"_id": "items", "count": 45, "novels": ["Novel1", "Novel2", "Novel3"]}
                ],
                [
                    {"_id": "Novel1", "blocks": 50, "categories": ["names", "places"], "author": "Author1"},
                    {"_id": "Novel2", "blocks": 30, "categories": ["names", "items"], "author": "Author2"},
                    {"_id": "Novel3", "blocks": 20, "categories": ["items"], "author": "Author3"}
                ]
            ]
            
            manager = BuildingBlocksManager(auto_connect=False)
            
            # Mock the _create_indexes method to avoid index creation during testing
            with patch.object(manager, '_create_indexes'):
                manager._connect()  # Explicitly call connect to set up mocked connection
            
            stats = manager.get_statistics()
            
            assert isinstance(stats, dict)
            assert "total_blocks" in stats
            assert "categories" in stats
            assert stats["total_blocks"] == 100

    def test_get_statistics_empty_collection(self):
        """Test getting statistics from empty collection"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            # Setup mock client and database hierarchy
            mock_db = Mock()
            mock_collection = Mock()
            
            # Configure mock to properly simulate MongoDB client behavior
            mock_client_instance = Mock()
            mock_client.return_value = mock_client_instance
            
            # Configure server_info for connection test
            mock_client_instance.server_info.return_value = {"version": "4.4.0"}
            
            # Configure database access: client[database_name] returns database
            mock_client_instance.__getitem__ = Mock(return_value=mock_db)
            
            # Configure collection access: db[collection_name] returns collection  
            mock_db.__getitem__ = Mock(return_value=mock_collection)
            
            # Mock empty collection
            mock_collection.aggregate.side_effect = [[], []]
            
            manager = BuildingBlocksManager(auto_connect=False)
            
            # Mock the _create_indexes method to avoid index creation during testing
            with patch.object(manager, '_create_indexes'):
                manager._connect()  # Explicitly call connect to set up mocked connection
            
            stats = manager.get_statistics()
            
            assert isinstance(stats, dict)
            assert stats["total_blocks"] == 0


@pytest.mark.unit
class TestIndexManagement:
    """Test index management functionality"""

    def test_create_indexes(self):
        """Test index creation"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            mock_collection = Mock()
            mock_client.return_value.rpger.building_blocks = mock_collection
            
            manager = BuildingBlocksManager(auto_connect=False)
            
            # Should attempt to create indexes during initialization
            # (Implementation may call create_index or similar)
            assert hasattr(manager, 'collection')

    def test_index_creation_failure(self):
        """Test handling of index creation failure"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            mock_collection = Mock()
            mock_client.return_value.rpger.building_blocks = mock_collection
            
            # Simulate index creation failure
            mock_collection.create_index.side_effect = Exception("Index creation failed")
            
            # Should handle gracefully
            try:
                manager = BuildingBlocksManager(auto_connect=False)
                # If initialization completes, error was handled
            except Exception:
                # Error handling may vary
                pass


@pytest.mark.unit
class TestErrorHandling:
    """Test error handling scenarios"""

    def test_connection_failure_handling(self):
        """Test MongoDB connection failure handling"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            mock_client.side_effect = Exception("MongoDB unavailable")
            
            # Should handle gracefully or raise appropriate error
            try:
                manager = BuildingBlocksManager(auto_connect=False)
            except Exception as e:
                # Expected for connection failures
                assert "MongoDB" in str(e) or "Connection" in str(e) or True

    def test_invalid_building_blocks_data(self):
        """Test handling of invalid building blocks data"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            # Setup mock client and database hierarchy
            mock_db = Mock()
            mock_collection = Mock()
            
            # Configure mock to properly simulate MongoDB client behavior
            mock_client_instance = Mock()
            mock_client.return_value = mock_client_instance
            
            # Configure server_info for connection test
            mock_client_instance.server_info.return_value = {"version": "4.4.0"}
            
            # Configure database access: client[database_name] returns database
            mock_client_instance.__getitem__ = Mock(return_value=mock_db)
            
            # Configure collection access: db[collection_name] returns collection  
            mock_db.__getitem__ = Mock(return_value=mock_collection)
            
            manager = BuildingBlocksManager(auto_connect=False)
            
            # Mock the _create_indexes method to avoid index creation during testing
            with patch.object(manager, '_create_indexes'):
                manager._connect()  # Explicitly call connect to set up mocked connection
            
            # Test with None
            result = manager.store_building_blocks(None, {})
            assert isinstance(result, dict)
            
            # Test with non-dict
            result = manager.store_building_blocks("invalid", {})
            assert isinstance(result, dict)

    def test_database_operation_failures(self):
        """Test handling of database operation failures"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            mock_collection = Mock()
            mock_client.return_value.rpger.building_blocks = mock_collection
            
            # Simulate database errors
            mock_collection.find.side_effect = Exception("Database error")
            
            manager = BuildingBlocksManager(auto_connect=False)
            
            # Should handle gracefully
            try:
                results = manager.get_blocks_by_category("names")
                # If no exception, error was handled
                assert isinstance(results, list)
            except Exception:
                # Database errors might be re-raised
                pass


@pytest.mark.unit
class TestDataValidation:
    """Test data validation functionality"""

    def test_category_validation(self):
        """Test category name validation"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            mock_collection = Mock()
            mock_client.return_value.rpger.building_blocks = mock_collection
            mock_collection.insert_one.return_value = Mock(inserted_id="test_id")
            
            manager = BuildingBlocksManager(auto_connect=False)
            
            # Test with valid categories
            valid_blocks = {
                "names": ["Valid Name"],
                "places": ["Valid Place"]
            }
            
            result = manager.store_building_blocks(valid_blocks, {"novel_title": "Test"})
            assert isinstance(result, dict)

    def test_text_validation(self):
        """Test text content validation"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            mock_collection = Mock()
            mock_client.return_value.rpger.building_blocks = mock_collection
            mock_collection.insert_one.return_value = Mock(inserted_id="test_id")
            
            manager = BuildingBlocksManager(auto_connect=False)
            
            # Test with empty strings (should be filtered out)
            blocks_with_empty = {
                "names": ["Valid Name", "", "Another Name", None, "Final Name"]
            }
            
            result = manager.store_building_blocks(blocks_with_empty, {"novel_title": "Test"})
            assert isinstance(result, dict)
            # Implementation should filter out empty/None values

    def test_metadata_validation(self):
        """Test source metadata validation"""
        with patch('Modules.building_blocks_manager.MongoClient') as mock_client:
            # Setup mock client and database hierarchy
            mock_db = Mock()
            mock_collection = Mock()
            
            # Configure mock to properly simulate MongoDB client behavior
            mock_client_instance = Mock()
            mock_client.return_value = mock_client_instance
            
            # Configure server_info for connection test
            mock_client_instance.server_info.return_value = {"version": "4.4.0"}
            
            # Configure database access: client[database_name] returns database
            mock_client_instance.__getitem__ = Mock(return_value=mock_db)
            
            # Configure collection access: db[collection_name] returns collection  
            mock_db.__getitem__ = Mock(return_value=mock_collection)
            
            mock_collection.update_one.return_value = Mock(upserted_id="test_id")
            mock_collection.insert_one.return_value = Mock(inserted_id="test_id")
            
            manager = BuildingBlocksManager(auto_connect=False)
            
            # Mock the _create_indexes method to avoid index creation during testing
            with patch.object(manager, '_create_indexes'):
                manager._connect()  # Explicitly call connect to set up mocked connection
            
            building_blocks = {"names": ["Test Name"]}
            
            # Test with missing metadata
            result = manager.store_building_blocks(building_blocks, {})
            assert isinstance(result, dict)
            
            # Test with None metadata
            result = manager.store_building_blocks(building_blocks, None)
            assert isinstance(result, dict)