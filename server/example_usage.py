#!/usr/bin/env python3
"""
Example usage of the Lazy Logistics Supplier Extraction API
"""

import requests
import json
import time
import os
from app.models.schemas import SupplierExtractionRequest, Supplier
from app.services.search import GoogleSearchService
from app.services.extraction import VertexAIExtractionService
from app.services.storage import FirestoreService
from app.utils.deduplication import SupplierDeduplicator
from dotenv import load_dotenv

# API configuration
API_BASE_URL = "http://localhost:8000"  # Change to your deployed URL

load_dotenv()

search_service = GoogleSearchService()
extraction_service = VertexAIExtractionService()
storage_service = FirestoreService()
deduplicator = SupplierDeduplicator()

def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check...")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_supplier_extraction(company_name: str, max_results: int = 20):
    """Test supplier extraction for a company."""
    print(f"Testing supplier extraction for: {company_name}")
    
    payload = {
        "company_name": company_name,
        "max_results": max_results
    }
    
    start_time = time.time()
    response = requests.post(f"{API_BASE_URL}/extract-suppliers", json=payload)
    end_time = time.time()
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Company: {result['company_name']}")
        print(f"Total suppliers found: {result['total_suppliers']}")
        print(f"Processing time: {result['processing_time']:.2f} seconds")
        print(f"API response time: {end_time - start_time:.2f} seconds")
        
        if result['suppliers']:
            print("\nSuppliers found:")
            for i, supplier in enumerate(result['suppliers'], 1):
                print(f"{i}. {supplier['name']}")
                print(f"   Confidence: {supplier['confidence']:.2f}")
                if supplier.get('context'):
                    print(f"   Context: {supplier['context']}")
                if supplier.get('source_url'):
                    print(f"   Source: {supplier['source_url']}")
                print()
        else:
            print("No suppliers found.")
    else:
        print(f"Error: {response.text}")
    
    print("-" * 50)

def test_extraction_history(company_name: str):
    """Test extraction history endpoint."""
    print(f"Testing extraction history for: {company_name}")
    
    response = requests.get(f"{API_BASE_URL}/history/{company_name}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"History entries: {len(result['history'])}")
        for entry in result['history'][:3]:  # Show first 3 entries
            print(f"- {entry['timestamp']}: {entry['total_suppliers']} suppliers")
    else:
        print(f"Error: {response.text}")
    
    print("-" * 50)

def test_statistics():
    """Test statistics endpoint."""
    print("Testing statistics endpoint...")
    
    response = requests.get(f"{API_BASE_URL}/statistics")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        stats = response.json()
        print(f"Total extractions: {stats['total_extractions']}")
        print(f"Cached companies: {stats['total_cached_companies']}")
        print(f"Timestamp: {stats['timestamp']}")
    else:
        print(f"Error: {response.text}")
    
    print("-" * 50)

def test_ignore_list_management():
    """Test ignore list management endpoints."""
    print("Testing ignore list management...")
    
    # Get current ignore list
    response = requests.get(f"{API_BASE_URL}/ignore-list")
    print(f"Get ignore list status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Current ignore list ({result['count']} items): {result['ignore_list']}")
    
    # Add a supplier to ignore list
    add_payload = {"supplier_name": "Test Ignore Supplier"}
    response = requests.post(f"{API_BASE_URL}/ignore-list/add", json=add_payload)
    print(f"Add to ignore list status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Add result: {result['message']}")
    
    # Get updated ignore list
    response = requests.get(f"{API_BASE_URL}/ignore-list")
    if response.status_code == 200:
        result = response.json()
        print(f"Updated ignore list ({result['count']} items): {result['ignore_list']}")
    
    # Remove the supplier from ignore list
    remove_payload = {"supplier_name": "Test Ignore Supplier"}
    response = requests.delete(f"{API_BASE_URL}/ignore-list/remove", json=remove_payload)
    print(f"Remove from ignore list status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Remove result: {result['message']}")
    
    print("-" * 50)

def main():
    """Run all example tests."""
    print("Lazy Logistics API - Example Usage")
    print("=" * 50)
    
    # Test health check
    test_health_check()
    
    # Test supplier extraction for different companies
    companies = ["Tesco", "Walmart", "Apple", "Nike"]
    
    for company in companies:
        test_supplier_extraction(company, max_results=20)
        time.sleep(1)  # Rate limiting
    
    # Test extraction history
    test_extraction_history("Tesco")
    
    # Test statistics
    test_statistics()
    
    # Test ignore list management
    test_ignore_list_management()
    
    print("Example usage completed!")

if __name__ == "__main__":
    main()

company_name = "Tesco"
max_results = 20

print(f"[DEBUG] Running pipeline for: {company_name}")

start_time = time.time()

# 1. Google Search
search_results = search_service.search_company_suppliers(company_name, max_results)
print("[DEBUG] Google Search Results:", search_results)

if not search_results:
    print("No search results.")
    exit(0)

# 2. Vertex AI Extraction
print("[DEBUG] Extraction input:", search_results)
raw_suppliers = extraction_service.extract_suppliers_from_search_results(company_name, search_results)
print("[DEBUG] Extraction output:", raw_suppliers)

# 3. Deduplication
print("[DEBUG] Deduplication input:", raw_suppliers)
deduplicated_suppliers = deduplicator.deduplicate_suppliers(raw_suppliers)
print("[DEBUG] Deduplication output:", deduplicated_suppliers)

# 4. Final output
supplier_models = [Supplier(**s) for s in deduplicated_suppliers]
processing_time = time.time() - start_time
print(f"[DEBUG] Final suppliers: {supplier_models}")
print(f"[DEBUG] Processing time: {processing_time:.2f}s") 