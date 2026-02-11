import json
import os
from typing import Dict, Any, Optional
from openai import OpenAI, APIError
from app.config import Config
from app.schemas import CRE_EXTRACTION_SCHEMA

class OpenAIExtractor:
    """Extract and structure CRE data using OpenAI's API with JSON mode"""
    
    def __init__(self):
        if not Config.validate_openai_config():
            raise ValueError("OpenAI API key not configured. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
        self.max_tokens = Config.OPENAI_MAX_TOKENS
    
    def extract_structured_data(self, text: str) -> Dict[str, Any]:
        """
        Extract structured CRE data from document text using OpenAI API.
        Returns JSON object with guaranteed structure based on schema, including citations.
        """
        if not text or len(text.strip()) == 0:
            return self._get_empty_response()
        
        try:
            # Chunk text if too large (accounting for tokens)
            text = self._prepare_text(text)
            
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                response_format={"type": "json_schema", "json_schema": CRE_EXTRACTION_SCHEMA},
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert commercial real estate analyst. Extract detailed CRE financial and operational metrics.

CRITICAL REQUIREMENTS:
1. For EVERY extracted value, include the exact source_text snippet from the document that supports it.
2. If a field is not mentioned, set value to null and source_text to null (unit should be null when value is null).
3. Always include a unit when the document provides one (e.g., USD, USD/SF/yr, %, acres, SF). If not stated, set unit to null.
4. Use null for missing information, not empty strings.
5. Convert currency values to numbers (remove $ and commas).
6. Convert percentages to numbers (e.g., 5.5% -> 5.5) and set unit to "%".
7. For dates, use YYYY-MM-DD format when possible.
8. For lists, include up to 5-10 items as allowed and provide source_text for each item.
9. Source_text must be an exact snippet from the document (25-200 characters).

Return a valid JSON object matching the specified schema with complete source_text coverage for every non-null value."""
                    },
                    {
                        "role": "user",
                        "content": f"""Extract structured CRE data from the following document text. For each value, return value, unit, and source_text.

Key fields to capture include (not limited to): total project cost, expected exit valuation, stabilized NOI, operating expenses,
acres, land square feet, gross building area, net rentable area, and expected rents.

Document text:
{text}

Remember: EVERY non-null value must have a corresponding source_text snippet from the document."""
                    }
                ]
            )
            
            # Parse the JSON response
            result = json.loads(response.choices[0].message.content)
            return result
            
        except APIError as e:
            raise Exception(f"OpenAI API error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse OpenAI response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Error extracting data with OpenAI: {str(e)}")
    
    def _prepare_text(self, text: str, max_chars: int = 16000) -> str:
        """
        Prepare text for OpenAI API by truncating if necessary.
        Approximately 16k characters = 4k tokens for GPT models
        """
        if len(text) > max_chars:
            # Keep the beginning and end, as they often contain important summaries
            mid_point = max_chars // 2
            text = text[:mid_point] + "\n...[document content truncated]...\n" + text[-mid_point:]
        
        return text
    
    def _get_empty_response(self) -> Dict[str, Any]:
        """Return empty response with correct structure including citations"""
        return {
            "property_details": {
                "property_address": {"value": None, "unit": None, "source_text": None},
                "property_type": {"value": None, "unit": None, "source_text": None},
                "square_footage": {"value": None, "unit": None, "source_text": None},
                "acres": {"value": None, "unit": None, "source_text": None},
                "land_square_feet": {"value": None, "unit": None, "source_text": None},
                "gross_building_area": {"value": None, "unit": None, "source_text": None},
                "net_rentable_area": {"value": None, "unit": None, "source_text": None},
                "year_built": {"value": None, "unit": None, "source_text": None},
                "units": {"value": None, "unit": None, "source_text": None},
                "occupancy_rate": {"value": None, "unit": None, "source_text": None}
            },
            "financial_metrics": {
                "noi_annual": {"value": None, "unit": None, "source_text": None},
                "stabilized_noi": {"value": None, "unit": None, "source_text": None},
                "cap_rate": {"value": None, "unit": None, "source_text": None},
                "purchase_price": {"value": None, "unit": None, "source_text": None},
                "appraised_value": {"value": None, "unit": None, "source_text": None},
                "annual_gross_income": {"value": None, "unit": None, "source_text": None},
                "operating_expenses": {"value": None, "unit": None, "source_text": None},
                "debt_service": {"value": None, "unit": None, "source_text": None},
                "dscr": {"value": None, "unit": None, "source_text": None},
                "irr": {"value": None, "unit": None, "source_text": None},
                "project_cost": {"value": None, "unit": None, "source_text": None},
                "expected_exit_valuation": {"value": None, "unit": None, "source_text": None},
                "expected_rents": []
            },
            "loan_details": {
                "loan_amount": {"value": None, "unit": None, "source_text": None},
                "interest_rate": {"value": None, "unit": None, "source_text": None},
                "loan_term_years": {"value": None, "unit": None, "source_text": None},
                "loan_type": {"value": None, "unit": None, "source_text": None},
                "lender": {"value": None, "unit": None, "source_text": None},
                "maturity_date": {"value": None, "unit": None, "source_text": None},
                "ltv": {"value": None, "unit": None, "source_text": None}
            },
            "tenant_information": {
                "major_tenants": [],
                "lease_terms": {"value": None, "unit": None, "source_text": None},
                "tenant_quality": {"value": None, "unit": None, "source_text": None}
            },
            "market_analysis": {
                "market": {"value": None, "unit": None, "source_text": None},
                "submarket": {"value": None, "unit": None, "source_text": None},
                "comparable_properties": [],
                "market_trends": []
            },
            "risk_assessment": {
                "identified_risks": [],
                "mitigation_strategies": []
            },
            "extraction_metadata": {
                "confidence_score": 0.0,
                "missing_fields": [],
                "fields_with_citations": 0,
                "fields_without_citations": 0,
                "citation_coverage_percent": 0.0
            }
        }
    
    def extract_with_confidence(self, text: str) -> Dict[str, Any]:
        """
        Extract data and assess confidence based on completeness and citation coverage.
        """
        result = self.extract_structured_data(text)
        
        # Calculate confidence score and citation statistics
        total_fields = self._count_total_fields()
        filled_fields = self._count_filled_fields(result)
        fields_with_citations = self._count_fields_with_citations(result)
        
        confidence = (filled_fields / total_fields * 100) if total_fields > 0 else 0
        citation_coverage = (fields_with_citations / filled_fields * 100) if filled_fields > 0 else 0
        
        result['extraction_metadata']['confidence_score'] = round(confidence, 2)
        result['extraction_metadata']['missing_fields'] = self._identify_missing_fields(result)
        result['extraction_metadata']['fields_with_citations'] = fields_with_citations
        result['extraction_metadata']['fields_without_citations'] = filled_fields - fields_with_citations
        result['extraction_metadata']['citation_coverage_percent'] = round(citation_coverage, 2)
        
        return result
    
    def _count_total_fields(self) -> int:
        """Count total extractable fields"""
        return 38  # Based on schema
    
    def _count_filled_fields(self, data: Dict[str, Any]) -> int:
        """Count non-null fields in extracted data"""
        count = 0
        
        def count_fields(obj):
            nonlocal count
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key in ('source_text', 'unit'):
                        continue
                    if value is None:
                        continue
                    elif isinstance(value, dict):
                        # Check if this is a value/citation pair
                        if 'value' in value:
                            if value['value'] is not None:
                                count += 1
                        else:
                            count_fields(value)
                    elif isinstance(value, list):
                        for item in value:
                            if item:
                                count += 1
                    else:
                        count += 1
            elif isinstance(obj, list):
                for item in obj:
                    if item:
                        count += 1
        
        count_fields(data)
        return count
    
    def _count_fields_with_citations(self, data: Dict[str, Any]) -> int:
        """Count fields that have both value and citation"""
        count = 0
        
        def count_citations(obj):
            nonlocal count
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, dict):
                        if 'value' in value and 'source_text' in value:
                            if value['value'] is not None and value['source_text'] is not None:
                                count += 1
                        else:
                            count_citations(value)
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict) and 'source_text' in item:
                                if item.get('source_text') is not None and any(v for k, v in item.items() if k not in ('source_text', 'unit') and v is not None):
                                    count += 1
        
        count_citations(data)
        return count
    
    def _identify_missing_fields(self, data: Dict[str, Any]) -> list:
        """Identify which fields are empty"""
        missing = []
        
        def check_fields(obj, prefix=""):
            for key, value in obj.items():
                field_path = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict):
                    if key in ("source_text", "unit"):
                        continue
                    check_fields(value, field_path)
                elif isinstance(value, list):
                    if not value:
                        missing.append(field_path)
                elif value is None:
                    missing.append(field_path)
        
        check_fields(data)
        return missing
