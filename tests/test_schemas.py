import pytest
from datetime import datetime
from app.models.schemas import (
    SupplierExtractionRequest,
    Supplier,
    SupplierExtractionResponse,
    HealthResponse
)

class TestSupplierExtractionRequest:
    def test_valid_request(self):
        request = SupplierExtractionRequest(
            company_name="Tesco",
            max_results=10
        )
        assert request.company_name == "Tesco"
        assert request.max_results == 10
    
    def test_default_max_results(self):
        request = SupplierExtractionRequest(company_name="Tesco")
        assert request.max_results == 10
    
    def test_invalid_company_name(self):
        with pytest.raises(ValueError):
            SupplierExtractionRequest(company_name="")

class TestSupplier:
    def test_valid_supplier(self):
        supplier = Supplier(
            name="ABC Corp",
            confidence=0.85,
            source_url="https://example.com",
            context="Main supplier for electronics"
        )
        assert supplier.name == "ABC Corp"
        assert supplier.confidence == 0.85
        assert supplier.source_url == "https://example.com"
        assert supplier.context == "Main supplier for electronics"
    
    def test_supplier_without_optional_fields(self):
        supplier = Supplier(name="ABC Corp", confidence=0.85)
        assert supplier.name == "ABC Corp"
        assert supplier.confidence == 0.85
        assert supplier.source_url is None
        assert supplier.context is None
    
    def test_invalid_confidence(self):
        with pytest.raises(ValueError):
            Supplier(name="ABC Corp", confidence=1.5)  # > 1.0
        
        with pytest.raises(ValueError):
            Supplier(name="ABC Corp", confidence=-0.1)  # < 0.0

class TestSupplierExtractionResponse:
    def test_valid_response(self):
        suppliers = [
            Supplier(name="ABC Corp", confidence=0.85),
            Supplier(name="XYZ Ltd", confidence=0.92)
        ]
        
        response = SupplierExtractionResponse(
            company_name="Tesco",
            suppliers=suppliers,
            total_suppliers=2,
            processing_time=1.5
        )
        
        assert response.company_name == "Tesco"
        assert len(response.suppliers) == 2
        assert response.total_suppliers == 2
        assert response.processing_time == 1.5
        assert isinstance(response.timestamp, datetime)

class TestHealthResponse:
    def test_valid_health_response(self):
        response = HealthResponse(status="healthy")
        assert response.status == "healthy"
        assert isinstance(response.timestamp, datetime) 