import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.models.schemas import (
    SupplierExtractionRequest, 
    SupplierExtractionResponse, 
    Supplier,
    HealthResponse,
    IgnoreListResponse,
    IgnoreListActionRequest,
    IgnoreListActionResponse
)
from app.services.search import GoogleSearchService
from app.services.extraction import VertexAIExtractionService
from app.services.storage import FirestoreService
from app.utils.deduplication import SupplierDeduplicator
from app.config import config

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Lazy Logistics - Supplier Extraction API",
    description="Extract supplier information for companies using GCP and Vertex AI",
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

# Initialize services
try:
    search_service = GoogleSearchService()
    extraction_service = VertexAIExtractionService()
    storage_service = FirestoreService()
    deduplicator = SupplierDeduplicator()
except Exception as e:
    print(f"Failed to initialize services: {e}")
    search_service = None
    extraction_service = None
    storage_service = None
    deduplicator = None

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy")

@app.post("/extract-suppliers", response_model=SupplierExtractionResponse)
async def extract_suppliers(request: SupplierExtractionRequest):
    """Extract supplier information for a given company."""
    
    if not all([search_service, extraction_service, storage_service, deduplicator]):
        raise HTTPException(status_code=500, detail="Services not properly initialized")
    
    start_time = time.time()
    
    try:
        # Check cache first
        cached_result = storage_service.get_cached_result(request.company_name)
        if cached_result:
            return SupplierExtractionResponse(
                company_name=request.company_name,
                suppliers=[Supplier(**s) for s in cached_result["suppliers"]],
                total_suppliers=cached_result["total_suppliers"],
                processing_time=cached_result["processing_time"]
            )
        
        # Search for company information
        search_results = search_service.search_company_suppliers(
            request.company_name, 
            request.max_results
        )
        print("[DEBUG] Google Search Results:", search_results)
        
        if not search_results:
            return SupplierExtractionResponse(
                company_name=request.company_name,
                suppliers=[],
                total_suppliers=0,
                processing_time=time.time() - start_time
            )
        
        # Extract suppliers from search results
        print("[DEBUG] Extraction input:", search_results)
        raw_suppliers = extraction_service.extract_suppliers_from_search_results(
            request.company_name, 
            search_results
        )
        print("[DEBUG] Extraction output:", raw_suppliers)
        
        # Deduplicate suppliers
        print("[DEBUG] Deduplication input:", raw_suppliers)
        deduplicated_suppliers = deduplicator.deduplicate_suppliers(raw_suppliers)
        print("[DEBUG] Deduplication output:", deduplicated_suppliers)
        
        # Convert to Pydantic models
        supplier_models = [Supplier(**s) for s in deduplicated_suppliers]
        
        processing_time = time.time() - start_time
        
        # Store result for audit trail
        storage_service.store_extraction_result(
            request.company_name,
            [s.model_dump() for s in supplier_models],
            processing_time,
            search_results
        )
        
        # Cache result
        storage_service.cache_result(
            request.company_name,
            [s.model_dump() for s in supplier_models],
            processing_time
        )
        
        return SupplierExtractionResponse(
            company_name=request.company_name,
            suppliers=supplier_models,
            total_suppliers=len(supplier_models),
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

@app.get("/history/{company_name}")
async def get_extraction_history(company_name: str, limit: int = 10):
    """Get extraction history for a company."""
    
    if not storage_service:
        raise HTTPException(status_code=500, detail="Storage service not initialized")
    
    try:
        history = storage_service.get_extraction_history(company_name, limit)
        return {"company_name": company_name, "history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")

@app.get("/statistics")
async def get_statistics():
    """Get basic statistics about extractions."""
    
    if not storage_service:
        raise HTTPException(status_code=500, detail="Storage service not initialized")
    
    try:
        stats = storage_service.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")

# Ignore List Management Endpoints

@app.get("/ignore-list", response_model=IgnoreListResponse)
async def get_ignore_list():
    """Get the current supplier ignore list."""
    try:
        ignore_list = config.get_ignore_list()
        return IgnoreListResponse(ignore_list=ignore_list, count=len(ignore_list))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get ignore list: {str(e)}")

@app.post("/ignore-list/add", response_model=IgnoreListActionResponse)
async def add_to_ignore_list(request: IgnoreListActionRequest):
    """Add a supplier to the ignore list."""
    try:
        success = config.add_to_ignore_list(request.supplier_name)
        if success:
            return IgnoreListActionResponse(
                message=f"Added '{request.supplier_name}' to ignore list", 
                success=True
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to add supplier to ignore list")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add to ignore list: {str(e)}")

@app.delete("/ignore-list/remove", response_model=IgnoreListActionResponse)
async def remove_from_ignore_list(request: IgnoreListActionRequest):
    """Remove a supplier from the ignore list."""
    try:
        success = config.remove_from_ignore_list(request.supplier_name)
        if success:
            return IgnoreListActionResponse(
                message=f"Removed '{request.supplier_name}' from ignore list", 
                success=True
            )
        else:
            raise HTTPException(status_code=404, detail="Supplier not found in ignore list")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove from ignore list: {str(e)}")

@app.post("/ignore-list/reload", response_model=IgnoreListActionResponse)
async def reload_ignore_list():
    """Reload the ignore list from file."""
    try:
        config.reload_ignore_list()
        return IgnoreListActionResponse(
            message="Ignore list reloaded successfully", 
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reload ignore list: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 