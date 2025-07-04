import pytest
from unittest.mock import patch, MagicMock
from app.config import Config
from app.utils.deduplication import SupplierDeduplicator

class TestConfig:
    def setup_method(self):
        self.config = Config()
    
    @patch('pathlib.Path.exists')
    @patch('builtins.open')
    def test_load_ignore_list(self, mock_open, mock_exists):
        """Test loading ignore list from file."""
        mock_exists.return_value = True
        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_file.__iter__.return_value = [
            "Supplier A",
            "# This is a comment",
            "Supplier B",
            "",
            "Supplier C"
        ]
        mock_open.return_value = mock_file
        
        config = Config()
        assert config.is_supplier_ignored("Supplier A")
        assert config.is_supplier_ignored("supplier a")  # Case insensitive
        assert config.is_supplier_ignored("Supplier B")
        assert config.is_supplier_ignored("Supplier C")
        assert not config.is_supplier_ignored("Supplier D")
    
    def test_add_to_ignore_list(self):
        """Test adding supplier to ignore list."""
        with patch('app.config.Path') as mock_path, patch('app.config.open', create=True) as mock_open:
            mock_path_instance = MagicMock()
            mock_path_instance.exists.return_value = False
            mock_path.return_value = mock_path_instance
            mock_file = MagicMock()
            mock_open.return_value = mock_file

            config = Config()
            success = config.add_to_ignore_list("New Supplier")
            assert success
            assert config.is_supplier_ignored("New Supplier")
            mock_file.__enter__().write.assert_called()
            call_args = mock_file.__enter__().write.call_args[0][0]
            assert call_args == "New Supplier\n"
    
    def test_remove_from_ignore_list(self):
        """Test removing supplier from ignore list."""
        with patch('pathlib.Path.exists', return_value=True):
            config = Config()
        
        # Add supplier first
        config._ignored_suppliers.add("test supplier")
        
        with patch('builtins.open', create=True) as mock_open:
            mock_file = MagicMock()
            mock_file.readlines.return_value = ["Test Supplier\n", "Other Supplier\n"]
            mock_open.return_value = mock_file
            
            success = config.remove_from_ignore_list("Test Supplier")
            assert success
            assert not config.is_supplier_ignored("Test Supplier")

class TestSupplierDeduplicatorWithIgnoreList:
    def setup_method(self):
        self.deduplicator = SupplierDeduplicator()
    
    @patch('app.config.config.is_supplier_ignored')
    def test_deduplicate_suppliers_with_ignored_suppliers(self, mock_is_ignored):
        """Test that ignored suppliers are filtered out."""
        suppliers = [
            {"name": "Good Supplier", "confidence": 0.8},
            {"name": "Ignored Supplier", "confidence": 0.9},
            {"name": "Another Good Supplier", "confidence": 0.7}
        ]
        
        # Mock ignore list behavior
        mock_is_ignored.side_effect = lambda name: name == "Ignored Supplier"
        
        result = self.deduplicator.deduplicate_suppliers(suppliers)
        
        # Should only return non-ignored suppliers
        assert len(result) == 2
        assert result[0]["name"] == "Good Supplier"
        assert result[1]["name"] == "Another Good Supplier"
        assert "Ignored Supplier" not in [s["name"] for s in result]
    
    @patch('app.config.config.is_supplier_ignored')
    def test_deduplicate_suppliers_all_ignored(self, mock_is_ignored):
        """Test when all suppliers are ignored."""
        suppliers = [
            {"name": "Ignored Supplier 1", "confidence": 0.8},
            {"name": "Ignored Supplier 2", "confidence": 0.9}
        ]
        
        # Mock all suppliers as ignored
        mock_is_ignored.return_value = True
        
        result = self.deduplicator.deduplicate_suppliers(suppliers)
        
        # Should return empty list
        assert result == []
    
    @patch('app.config.config.is_supplier_ignored')
    def test_deduplicate_suppliers_case_insensitive_ignore(self, mock_is_ignored):
        """Test that ignore list is case insensitive."""
        suppliers = [
            {"name": "SUPPLIER A", "confidence": 0.8},
            {"name": "supplier b", "confidence": 0.9}
        ]
        
        # Mock ignore list behavior (case insensitive)
        mock_is_ignored.side_effect = lambda name: name.lower() == "supplier a"
        
        result = self.deduplicator.deduplicate_suppliers(suppliers)
        
        # Should only return supplier b
        assert len(result) == 1
        assert result[0]["name"] == "supplier b" 