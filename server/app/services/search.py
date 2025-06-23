import os
import requests
from typing import List, Dict, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleSearchService:
    def __init__(self):
        self.api_key = os.getenv("CUSTOM_SEARCH_API_KEY")
        self.search_engine_id = os.getenv("CUSTOM_SEARCH_ENGINE_ID")
        
        if not self.api_key or not self.search_engine_id:
            raise ValueError("CUSTOM_SEARCH_API_KEY and CUSTOM_SEARCH_ENGINE_ID must be set")
    
    def search_company_suppliers(self, company_name: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for web documents mentioning the company and potential suppliers."""
        
        try:
            # Build the service
            service = build("customsearch", "v1", developerKey=self.api_key)
            
            # Search query to find supplier information
            query = f'"{company_name}" suppliers vendors partners supply chain'
            
            # Execute search
            result = service.cse().list(
                q=query,
                cx=self.search_engine_id,
                num=min(max_results, 10)  # Google CSE max is 10 per request
            ).execute()
            
            # Extract search results
            search_results = []
            for item in result.get("items", []):
                search_results.append({
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "link": item.get("link", ""),
                    "displayLink": item.get("displayLink", "")
                })
            
            return search_results
            
        except HttpError as e:
            print(f"Google Search API error: {e}")
            return []
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def get_document_content(self, url: str) -> str:
        """Fetch document content from URL (simplified - in production, use proper web scraping)"""
        try:
            response = requests.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (compatible; LazyLogistics/1.0)"
            })
            response.raise_for_status()
            return response.text[:5000]  # Limit content length
        except Exception as e:
            print(f"Error fetching content from {url}: {e}")
            return "" 