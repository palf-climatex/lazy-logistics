#!/usr/bin/env python3
"""
Example usage of the Lazy Logistics Supplier Extraction API
"""

import requests
import json
import time

# API configuration
API_BASE_URL = "http://localhost:8000"  # Change to your deployed URL

def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check...")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_supplier_extraction(company_name: str, max_results: int = 5):
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

def main():
    """Run all example tests."""
    print("Lazy Logistics API - Example Usage")
    print("=" * 50)
    
    # Test health check
    test_health_check()
    
    # Test supplier extraction for different companies
    companies = ["Tesco", "Walmart", "Apple", "Nike"]
    
    for company in companies:
        test_supplier_extraction(company, max_results=3)
        time.sleep(1)  # Rate limiting
    
    # Test extraction history
    test_extraction_history("Tesco")
    
    # Test statistics
    test_statistics()
    
    print("Example usage completed!")

if __name__ == "__main__":
    main() 