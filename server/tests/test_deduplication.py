import pytest
from app.utils.deduplication import SupplierDeduplicator

class TestSupplierDeduplicator:
    def setup_method(self):
        self.deduplicator = SupplierDeduplicator(similarity_threshold=80.0)
    
    def test_normalize_company_name(self):
        # Test basic normalization
        assert self.deduplicator._normalize_company_name("ABC Corp") == "abc"
        assert self.deduplicator._normalize_company_name("XYZ Technologies Inc.") == "xyz"
        assert self.deduplicator._normalize_company_name("Test Company Ltd.") == "test company"
        
        # Test with special characters - these get converted to spaces
        assert self.deduplicator._normalize_company_name("A&B Corp.") == "a b"
        assert self.deduplicator._normalize_company_name("Test-Company") == "test company"
    
    def test_deduplicate_suppliers_no_duplicates(self):
        suppliers = [
            {"name": "ABC Corp", "confidence": 0.8, "source_url": "http://example1.com"},
            {"name": "XYZ Ltd", "confidence": 0.9, "source_url": "http://example2.com"}
        ]
        
        result = self.deduplicator.deduplicate_suppliers(suppliers)
        assert len(result) == 2
        assert result[0]["name"] == "ABC Corp"
        assert result[1]["name"] == "XYZ Ltd"
    
    def test_deduplicate_suppliers_with_duplicates(self):
        suppliers = [
            {"name": "ABC Corp", "confidence": 0.8, "source_url": "http://example1.com"},
            {"name": "ABC Corp", "confidence": 0.9, "source_url": "http://example2.com"},  # Exact duplicate
            {"name": "XYZ Ltd", "confidence": 0.7, "source_url": "http://example3.com"}
        ]
        
        result = self.deduplicator.deduplicate_suppliers(suppliers)
        assert len(result) == 2  # ABC Corp should be merged, XYZ Ltd separate
        # Check that ABC Corp was merged (should have higher confidence name)
        abc_suppliers = [s for s in result if "ABC" in s["name"]]
        assert len(abc_suppliers) == 1
        assert abc_suppliers[0]["confidence"] == 0.85  # Average of 0.8 and 0.9
    
    def test_deduplicate_suppliers_empty_list(self):
        result = self.deduplicator.deduplicate_suppliers([])
        assert result == []
    
    def test_deduplicate_suppliers_single_item(self):
        suppliers = [{"name": "ABC Corp", "confidence": 0.8}]
        result = self.deduplicator.deduplicate_suppliers(suppliers)
        assert len(result) == 1
        assert result[0]["name"] == "ABC Corp"
        assert "normalized_name" not in result[0]  # Should be removed
    
    def test_merge_supplier_group(self):
        group = [
            {"name": "ABC Corp", "confidence": 0.8, "source_url": "http://example1.com", "context": "Main supplier"},
            {"name": "ABC Corporation", "confidence": 0.9, "source_url": "http://example2.com", "context": "Primary vendor"}
        ]
        
        result = self.deduplicator._merge_supplier_group(group)
        assert result["name"] == "ABC Corporation"  # Higher confidence
        assert result["confidence"] == 0.85  # Average
        assert result["source_url"] == "http://example1.com"  # First source
        assert result["context"] == "Main supplier; Primary vendor"  # Merged contexts
    
    def test_group_similar_suppliers(self):
        suppliers = [
            {"name": "ABC Corp", "normalized_name": "abc", "confidence": 0.8},
            {"name": "ABC Corporation", "normalized_name": "abc", "confidence": 0.9},
            {"name": "XYZ Ltd", "normalized_name": "xyz", "confidence": 0.7}
        ]
        
        groups = self.deduplicator._group_similar_suppliers(suppliers)
        assert len(groups) == 2
        assert len(groups[0]) == 2  # ABC Corp and ABC Corporation
        assert len(groups[1]) == 1  # XYZ Ltd 