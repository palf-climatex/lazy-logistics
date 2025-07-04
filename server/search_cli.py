#!/usr/bin/env python3
"""
Command line interface for supplier search functionality.
Usage: python search_cli.py "Company Name" [max_results]
"""

import sys
import os
import json
from dotenv import load_dotenv
from app.services.search import GoogleSearchService
from app.services.extraction import VertexAIExtractionService
from app.utils.deduplication import SupplierDeduplicator
from app.models.schemas import Supplier

def main():
    """Main CLI function."""
    load_dotenv()
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python search_cli.py 'Company Name' [max_results]")
        print("Example: python search_cli.py 'Tesco' 20")
        sys.exit(1)
    
    company_name = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    print(f"Searching for suppliers of: {company_name}")
    print(f"Maximum results: {max_results}")
    print("-" * 50)
    
    try:
        # Initialize services
        search_service = GoogleSearchService()
        extraction_service = VertexAIExtractionService()
        deduplicator = SupplierDeduplicator()
        
        # Step 1: Search for company information
        print("1. Searching web for company supplier information...")
        search_results = search_service.search_company_suppliers(company_name, max_results)
        print(f"   Found {len(search_results)} search results")
        
        if not search_results:
            print("   No search results found.")
            return
        
        # Step 2: Extract suppliers from search results
        print("2. Extracting suppliers from search results...")
        raw_suppliers = extraction_service.extract_suppliers_from_search_results(
            company_name, search_results
        )
        print(f"   Extracted {len(raw_suppliers)} raw suppliers")
        
        if not raw_suppliers:
            print("   No suppliers extracted.")
            return
        
        # Step 3: Deduplicate suppliers
        print("3. Deduplicating suppliers...")
        deduplicated_suppliers = deduplicator.deduplicate_suppliers(raw_suppliers)
        print(f"   Final result: {len(deduplicated_suppliers)} unique suppliers")
        
        # Step 4: Display results
        print("\n" + "=" * 50)
        print("SUPPLIER EXTRACTION RESULTS")
        print("=" * 50)
        
        if deduplicated_suppliers:
            for i, supplier_data in enumerate(deduplicated_suppliers, 1):
                supplier = Supplier(**supplier_data)
                print(f"\n{i}. {supplier.name}")
                print(f"   Confidence: {supplier.confidence:.2f}")
                if supplier.context:
                    print(f"   Context: {supplier.context}")
                if supplier.source_url:
                    print(f"   Source: {supplier.source_url}")
        else:
            print("No suppliers found.")
        
        # Optional: Save results to JSON file
        output_file = f"suppliers_{company_name.lower().replace(' ', '_')}.json"
        with open(output_file, 'w') as f:
            json.dump({
                "company_name": company_name,
                "max_results": max_results,
                "total_suppliers": len(deduplicated_suppliers),
                "suppliers": [s.model_dump() for s in [Supplier(**s) for s in deduplicated_suppliers]]
            }, f, indent=2)
        print(f"\nResults saved to: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 