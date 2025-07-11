from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime, UTC

class SupplierExtractionRequest(BaseModel):
    company_name: str = Field(..., description="Name of the company to extract suppliers for")
    max_results: int = Field(default=20, description="Maximum number of search results to process")
    
    @field_validator('company_name')
    @classmethod
    def validate_company_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Company name cannot be empty')
        return v.strip()

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
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

# Ignore List Schemas

class IgnoreListResponse(BaseModel):
    ignore_list: List[str] = Field(..., description="List of ignored supplier names")
    count: int = Field(..., description="Number of suppliers in ignore list")

class IgnoreListActionRequest(BaseModel):
    supplier_name: str = Field(..., description="Name of the supplier to add/remove")
    
    @field_validator('supplier_name')
    @classmethod
    def validate_supplier_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Supplier name cannot be empty')
        return v.strip()

class IgnoreListActionResponse(BaseModel):
    message: str = Field(..., description="Response message")
    success: bool = Field(..., description="Whether the action was successful") 