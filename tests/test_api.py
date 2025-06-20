import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

class TestAPIEndpoints:
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    @patch('app.main.search_service')
    @patch('app.main.extraction_service')
    @patch('app.main.storage_service')
    @patch('app.main.deduplicator')
    def test_extract_suppliers_success(self, mock_deduplicator, mock_storage, mock_extraction, mock_search):
        """Test successful supplier extraction."""
        # Mock cache miss
        mock_storage.get_cached_result.return_value = None
        
        # Mock search results
        mock_search.search_company_suppliers.return_value = [
            {
                "title": "Tesco Suppliers",
                "snippet": "Tesco works with ABC Corp and XYZ Ltd",
                "link": "http://example.com",
                "displayLink": "example.com"
            }
        ]
        
        # Mock extraction results
        mock_extraction.extract_suppliers_from_search_results.return_value = [
            {"name": "ABC Corp", "confidence": 0.85, "context": "Main supplier"},
            {"name": "XYZ Ltd", "confidence": 0.92, "context": "Technology partner"}
        ]
        
        # Mock deduplication
        mock_deduplicator.deduplicate_suppliers.return_value = [
            {"name": "ABC Corp", "confidence": 0.85, "context": "Main supplier"},
            {"name": "XYZ Ltd", "confidence": 0.92, "context": "Technology partner"}
        ]
        
        response = client.post("/extract-suppliers", json={
            "company_name": "Tesco",
            "max_results": 5
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["company_name"] == "Tesco"
        assert data["total_suppliers"] == 2
        assert len(data["suppliers"]) == 2
        assert data["suppliers"][0]["name"] == "ABC Corp"
        assert data["suppliers"][1]["name"] == "XYZ Ltd"
        assert "processing_time" in data
    
    @patch('app.main.storage_service')
    def test_extract_suppliers_cache_hit(self, mock_storage):
        """Test supplier extraction with cache hit."""
        # Mock cache hit
        mock_storage.get_cached_result.return_value = {
            "suppliers": [
                {"name": "ABC Corp", "confidence": 0.85, "context": "Cached result"}
            ],
            "total_suppliers": 1,
            "processing_time": 0.5
        }
        
        response = client.post("/extract-suppliers", json={
            "company_name": "Tesco",
            "max_results": 5
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["company_name"] == "Tesco"
        assert data["total_suppliers"] == 1
        assert len(data["suppliers"]) == 1
        assert data["suppliers"][0]["name"] == "ABC Corp"
    
    @patch('app.main.search_service')
    def test_extract_suppliers_no_results(self, mock_search):
        """Test supplier extraction with no search results."""
        # Mock empty search results
        mock_search.search_company_suppliers.return_value = []
        
        response = client.post("/extract-suppliers", json={
            "company_name": "UnknownCompany",
            "max_results": 5
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["company_name"] == "UnknownCompany"
        assert data["total_suppliers"] == 0
        assert len(data["suppliers"]) == 0
    
    def test_extract_suppliers_invalid_request(self):
        """Test supplier extraction with invalid request."""
        response = client.post("/extract-suppliers", json={
            "company_name": "",  # Invalid empty name
            "max_results": 5
        })
        
        assert response.status_code == 422  # Validation error
    
    @patch('app.main.storage_service')
    def test_extraction_history(self, mock_storage):
        """Test extraction history endpoint."""
        mock_storage.get_extraction_history.return_value = [
            {
                "timestamp": "2024-01-01T10:00:00",
                "total_suppliers": 3,
                "processing_time": 1.5
            },
            {
                "timestamp": "2024-01-02T10:00:00",
                "total_suppliers": 2,
                "processing_time": 1.2
            }
        ]
        
        response = client.get("/history/Tesco")
        assert response.status_code == 200
        data = response.json()
        assert data["company_name"] == "Tesco"
        assert len(data["history"]) == 2
        assert data["history"][0]["total_suppliers"] == 3
    
    @patch('app.main.storage_service')
    def test_statistics(self, mock_storage):
        """Test statistics endpoint."""
        mock_storage.get_statistics.return_value = {
            "total_extractions": 100,
            "total_cached_companies": 25,
            "timestamp": "2024-01-01T10:00:00"
        }
        
        response = client.get("/statistics")
        assert response.status_code == 200
        data = response.json()
        assert data["total_extractions"] == 100
        assert data["total_cached_companies"] == 25
        assert "timestamp" in data
    
    def test_services_not_initialized(self):
        """Test behavior when services are not initialized."""
        # Temporarily set services to None
        original_search = app.dependency_overrides.get("search_service")
        original_extraction = app.dependency_overrides.get("extraction_service")
        original_storage = app.dependency_overrides.get("storage_service")
        original_deduplicator = app.dependency_overrides.get("deduplicator")
        
        try:
            # Override services to None
            app.dependency_overrides["search_service"] = lambda: None
            app.dependency_overrides["extraction_service"] = lambda: None
            app.dependency_overrides["storage_service"] = lambda: None
            app.dependency_overrides["deduplicator"] = lambda: None
            
            response = client.post("/extract-suppliers", json={
                "company_name": "Tesco",
                "max_results": 5
            })
            
            assert response.status_code == 500
            assert "Services not properly initialized" in response.json()["detail"]
        
        finally:
            # Restore original services
            if original_search:
                app.dependency_overrides["search_service"] = original_search
            if original_extraction:
                app.dependency_overrides["extraction_service"] = original_extraction
            if original_storage:
                app.dependency_overrides["storage_service"] = original_storage
            if original_deduplicator:
                app.dependency_overrides["deduplicator"] = original_deduplicator 