import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.models.schemas import (
    SupplierExtractionRequest, 
    SupplierExtractionResponse, 
    Supplier,
    HealthResponse
)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Lazy Logistics - Supplier Extraction API (Mock)",
    description="Mock version for testing without GCP services",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy")

@app.post("/extract-suppliers", response_model=SupplierExtractionResponse)
async def extract_suppliers(request: SupplierExtractionRequest):
    """Mock supplier extraction for testing."""
    
    start_time = time.time()
    
    # Mock response based on company name
    mock_suppliers = {
        "tesco": [
            {"name": "ABC Food Corp", "confidence": 0.85, "context": "Main food supplier"},
            {"name": "XYZ Logistics", "confidence": 0.92, "context": "Transportation partner"},
            {"name": "Fresh Produce Ltd", "confidence": 0.78, "context": "Fresh food supplier"}
        ],
        "walmart": [
            {"name": "Global Supply Co", "confidence": 0.88, "context": "International supplier"},
            {"name": "Tech Solutions Inc", "confidence": 0.91, "context": "Technology partner"},
            {"name": "Manufacturing Corp", "confidence": 0.82, "context": "Manufacturing supplier"}
        ],
        "apple": [
            {"name": "Foxconn", "confidence": 0.95, "context": "Main manufacturing partner"},
            {"name": "Samsung Electronics", "confidence": 0.89, "context": "Component supplier"},
            {"name": "TSMC", "confidence": 0.93, "context": "Chip manufacturer"}
        ]
    }
    
    # Get mock suppliers for the company (case insensitive)
    company_key = request.company_name.lower()
    suppliers_data = mock_suppliers.get(company_key, [
        {"name": "Mock Supplier 1", "confidence": 0.75, "context": "Mock supplier for testing"},
        {"name": "Mock Supplier 2", "confidence": 0.80, "context": "Another mock supplier"}
    ])
    
    # Convert to Pydantic models
    supplier_models = [Supplier(**s) for s in suppliers_data]
    
    processing_time = time.time() - start_time
    
    return SupplierExtractionResponse(
        company_name=request.company_name,
        suppliers=supplier_models,
        total_suppliers=len(supplier_models),
        processing_time=processing_time
    )

@app.get("/history/{company_name}")
async def get_extraction_history(company_name: str, limit: int = 10):
    """Mock extraction history."""
    return {
        "company_name": company_name,
        "history": [
            {
                "timestamp": "2024-01-01T10:00:00",
                "total_suppliers": 3,
                "processing_time": 0.5
            }
        ]
    }

@app.get("/statistics")
async def get_statistics():
    """Mock statistics."""
    return {
        "total_extractions": 10,
        "total_cached_companies": 3,
        "timestamp": "2024-01-01T10:00:00"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 