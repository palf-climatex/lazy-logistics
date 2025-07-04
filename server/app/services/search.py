import os
import requests
from typing import List, Dict, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.config import MAX_SEARCH_RESULTS

class GoogleSearchService:
    def __init__(self):
        self.api_key = os.getenv("CUSTOM_SEARCH_API_KEY")
        self.search_engine_id = os.getenv("CUSTOM_SEARCH_ENGINE_ID")
        
        if not self.api_key or not self.search_engine_id:
            raise ValueError("CUSTOM_SEARCH_API_KEY and CUSTOM_SEARCH_ENGINE_ID must be set")
    
    def search_company_suppliers(self, company_name: str, max_results: int = MAX_SEARCH_RESULTS) -> List[Dict[str, Any]]:
        """Search for web documents mentioning the company and potential suppliers. Fetch up to MAX_SEARCH_RESULTS results."""
        try:
            service = build("customsearch", "v1", developerKey=self.api_key)
            query = f'"{company_name}" suppliers vendors partners supply chain'
            search_results = []
            results_per_page = 10
            total_to_fetch = min(max_results, MAX_SEARCH_RESULTS)
            for start in range(1, total_to_fetch + 1, results_per_page):
                result = service.cse().list(
                    q=query,
                    cx=self.search_engine_id,
                    num=results_per_page,
                    start=start
                ).execute()
                for item in result.get("items", []):
                    search_results.append({
                        "title": item.get("title", ""),
                        "snippet": item.get("snippet", ""),
                        "link": item.get("link", ""),
                        "displayLink": item.get("displayLink", "")
                    })
                if len(search_results) >= total_to_fetch or not result.get("items"):
                    break
            return search_results[:total_to_fetch]
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