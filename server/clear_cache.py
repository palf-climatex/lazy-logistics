#!/usr/bin/env python3
"""
Script to clear all caches in Firestore.
Usage: python clear_cache.py [company_name]
If no company_name is provided, clears all caches.
"""

import sys
from dotenv import load_dotenv
from app.services.storage import FirestoreService

def clear_all_caches():
    """Clear all cached results."""
    try:
        storage_service = FirestoreService()
        
        # Get all cache documents
        cache_docs = storage_service.cache_collection.stream()
        count = 0
        
        for doc in cache_docs:
            doc.reference.delete()
            count += 1
            print(f"Deleted cache for: {doc.id}")
        
        print(f"\nCleared {count} cache entries.")
        
    except Exception as e:
        print(f"Error clearing caches: {e}")
        return False
    
    return True

def clear_company_cache(company_name: str):
    """Clear cache for a specific company."""
    try:
        storage_service = FirestoreService()
        
        # Delete the specific company's cache
        doc_ref = storage_service.cache_collection.document(company_name.lower())
        doc = doc_ref.get()
        
        if doc.exists:
            doc_ref.delete()
            print(f"Cache cleared for: {company_name}")
        else:
            print(f"No cache found for: {company_name}")
        
    except Exception as e:
        print(f"Error clearing cache for {company_name}: {e}")
        return False
    
    return True

def main():
    """Main function."""
    load_dotenv()
    
    if len(sys.argv) > 1:
        company_name = sys.argv[1]
        print(f"Clearing cache for: {company_name}")
        success = clear_company_cache(company_name)
    else:
        print("Clearing all caches...")
        success = clear_all_caches()
    
    if success:
        print("Cache clearing completed successfully.")
    else:
        print("Cache clearing failed.")
        sys.exit(1)

if __name__ == "__main__":
    main() 