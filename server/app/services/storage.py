import os
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from google.cloud import firestore

class FirestoreService:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT must be set")
        
        self.db = firestore.Client(project=self.project_id)
        self.extractions_collection = self.db.collection("supplier_extractions")
        self.cache_collection = self.db.collection("cache")
    
    def store_extraction_result(self, company_name: str, suppliers: List[Dict[str, Any]], 
                              processing_time: float, search_results: List[Dict[str, Any]]) -> str:
        """Store extraction result in Firestore for audit trail."""
        
        doc_data = {
            "company_name": company_name,
            "suppliers": suppliers,
            "total_suppliers": len(suppliers),
            "processing_time": processing_time,
            "search_results_count": len(search_results),
            "timestamp": datetime.now(timezone.utc),
            "search_results": search_results
        }
        
        doc_ref = self.extractions_collection.add(doc_data)
        return doc_ref[1].id
    
    def get_cached_result(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Get cached extraction result for a company."""
        
        # Check if we have a recent cache entry (within 24 hours)
        cache_doc = self.cache_collection.document(company_name.lower()).get()
        
        if cache_doc.exists:
            cache_data = cache_doc.to_dict()
            cache_time = cache_data.get("timestamp")
            
            # Check if cache is still valid (24 hours)
            if cache_time and (datetime.now(timezone.utc) - cache_time).days < 1:
                return cache_data
        
        return None
    
    def cache_result(self, company_name: str, suppliers: List[Dict[str, Any]], 
                    processing_time: float) -> None:
        """Cache extraction result for faster future access."""
        
        cache_data = {
            "company_name": company_name,
            "suppliers": suppliers,
            "total_suppliers": len(suppliers),
            "processing_time": processing_time,
            "timestamp": datetime.now(timezone.utc)
        }
        
        self.cache_collection.document(company_name.lower()).set(cache_data)
    
    def get_extraction_history(self, company_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get extraction history for a company."""
        
        query = (self.extractions_collection
                .where("company_name", "==", company_name)
                .order_by("timestamp", direction=firestore.Query.DESCENDING)
                .limit(limit))
        
        docs = query.stream()
        return [doc.to_dict() for doc in docs]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get basic statistics about extractions."""
        
        total_extractions = len(list(self.extractions_collection.stream()))
        total_cached = len(list(self.cache_collection.stream()))
        
        return {
            "total_extractions": total_extractions,
            "total_cached_companies": total_cached,
            "timestamp": datetime.now(timezone.utc)
        } 