from typing import List, Dict, Any
from fuzzywuzzy import fuzz
import re

class SupplierDeduplicator:
    def __init__(self, similarity_threshold: float = 80.0):
        self.similarity_threshold = similarity_threshold
    
    def deduplicate_suppliers(self, suppliers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate suppliers using fuzzy string matching."""
        
        if not suppliers:
            return []
        
        # Normalize supplier names
        normalized_suppliers = []
        for supplier in suppliers:
            normalized_name = self._normalize_company_name(supplier["name"])
            normalized_suppliers.append({
                **supplier,
                "normalized_name": normalized_name
            })
        
        # Group similar suppliers
        grouped_suppliers = self._group_similar_suppliers(normalized_suppliers)
        
        # Merge groups into final suppliers
        final_suppliers = []
        for group in grouped_suppliers:
            merged_supplier = self._merge_supplier_group(group)
            final_suppliers.append(merged_supplier)
        
        return final_suppliers
    
    def _normalize_company_name(self, name: str) -> str:
        """Normalize company name for comparison."""
        
        # Convert to lowercase
        normalized = name.lower()
        
        # Replace hyphens and other separators with spaces
        normalized = re.sub(r'[-_&]', ' ', normalized)
        
        # Remove extra whitespace and punctuation (except spaces)
        normalized = re.sub(r'[^\w\s]', '', normalized)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        # Remove common business suffixes only if at the end
        suffixes = [
            r' inc\.?$', r' corp\.?$', r' llc$', r' ltd\.?$', 
            r' limited$', r' co\.?$', r' group$',
            r' international$', r' intl\.?$', r' technologies$',
            r' tech$', r' systems$', r' solutions$'
        ]
        
        for suffix in suffixes:
            normalized = re.sub(suffix, '', normalized)
        
        return normalized
    
    def _group_similar_suppliers(self, suppliers: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """Group suppliers with similar names."""
        
        groups = []
        used_indices = set()
        
        for i, supplier in enumerate(suppliers):
            if i in used_indices:
                continue
            
            group = [supplier]
            used_indices.add(i)
            
            # Find similar suppliers
            for j, other_supplier in enumerate(suppliers):
                if j in used_indices:
                    continue
                
                similarity = fuzz.ratio(
                    supplier["normalized_name"], 
                    other_supplier["normalized_name"]
                )
                
                if similarity >= self.similarity_threshold:
                    group.append(other_supplier)
                    used_indices.add(j)
            
            groups.append(group)
        
        return groups
    
    def _merge_supplier_group(self, group: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge a group of similar suppliers into one."""
        
        if len(group) == 1:
            # Remove normalized_name from output
            result = {k: v for k, v in group[0].items() if k != "normalized_name"}
            return result
        
        # Use the supplier with highest confidence as base
        best_supplier = max(group, key=lambda x: x.get("confidence", 0))
        
        # Merge source URLs and contexts
        all_sources = []
        all_contexts = []
        
        for supplier in group:
            if supplier.get("source_url"):
                all_sources.append(supplier["source_url"])
            if supplier.get("context"):
                all_contexts.append(supplier["context"])
        
        # Calculate average confidence
        avg_confidence = sum(s.get("confidence", 0) for s in group) / len(group)
        
        merged = {
            "name": best_supplier["name"],
            "confidence": round(avg_confidence, 2),  # Round to avoid floating point issues
            "source_url": all_sources[0] if all_sources else None,
            "context": "; ".join(all_contexts) if all_contexts else None
        }
        
        return merged 