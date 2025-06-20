from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class SupplierExtractionRequest(BaseModel):
    company_name: str = Field(..., description="Name of the company to extract suppliers for")
    max_results: int = Field(default=10, description="Maximum number of search results to process")

class Supplier(BaseModel):
    name: str = Field(..., description="Supplier company name")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score for extraction")
    source_url: Optional[str] = Field(None, description="Source URL where supplier was mentioned")
    context: Optional[str] = Field(None, description="Context snippet where supplier was found")

class SupplierExtractionResponse(BaseModel):
    company_name: str
    suppliers: List[Supplier]
    total_suppliers: int
    processing_time: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow) 