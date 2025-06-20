import os
import json
from typing import List, Dict, Any
from google.cloud import aiplatform
from vertexai.language_models import TextGenerationModel

class VertexAIExtractionService:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT must be set")
        
        # Initialize Vertex AI
        aiplatform.init(project=self.project_id)
        self.model = TextGenerationModel.from_pretrained("gemini-1.5-pro")
    
    def extract_suppliers_from_text(self, company_name: str, text_content: str, source_url: str = "") -> List[Dict[str, Any]]:
        """Extract supplier names from text content using Vertex AI Gemini."""
        
        prompt = self._build_extraction_prompt(company_name, text_content, source_url)
        
        try:
            response = self.model.predict(prompt, max_output_tokens=2048, temperature=0.1)
            
            # Parse the JSON response
            try:
                result = json.loads(response.text)
                return result.get("suppliers", [])
            except json.JSONDecodeError:
                print(f"Failed to parse JSON response: {response.text}")
                return []
                
        except Exception as e:
            print(f"Vertex AI extraction error: {e}")
            return []
    
    def _build_extraction_prompt(self, company_name: str, text_content: str, source_url: str) -> str:
        """Build the prompt for supplier extraction."""
        
        return f"""
You are an expert at extracting supplier information from business documents. Your task is to identify any supplier companies mentioned in relation to "{company_name}".

TEXT TO ANALYZE:
{text_content}

SOURCE: {source_url}

INSTRUCTIONS:
1. Identify any company names that appear to be suppliers, vendors, or business partners of "{company_name}"
2. Focus on companies that provide goods, services, or materials to "{company_name}"
3. Exclude "{company_name}" itself and its subsidiaries
4. For each supplier, provide:
   - Company name (normalized)
   - Confidence score (0.0-1.0)
   - Brief context of the relationship

OUTPUT FORMAT (JSON only):
{{
    "suppliers": [
        {{
            "name": "Supplier Company Name",
            "confidence": 0.85,
            "context": "Brief description of relationship or mention context"
        }}
    ]
}}

IMPORTANT: Return ONLY valid JSON. Do not include any other text or explanations.
"""
    
    def extract_suppliers_from_search_results(self, company_name: str, search_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract suppliers from multiple search results."""
        
        all_suppliers = []
        
        for result in search_results:
            # Combine title and snippet for analysis
            content = f"Title: {result.get('title', '')}\nSnippet: {result.get('snippet', '')}"
            source_url = result.get('link', '')
            
            suppliers = self.extract_suppliers_from_text(company_name, content, source_url)
            
            # Add source URL to each supplier
            for supplier in suppliers:
                supplier['source_url'] = source_url
            
            all_suppliers.extend(suppliers)
        
        return all_suppliers 