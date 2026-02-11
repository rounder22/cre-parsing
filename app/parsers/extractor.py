import re
from typing import Dict, Any, List, Optional
from app.parsers.pdf_parser import PDFParser
from app.parsers.word_parser import WordParser
from app.parsers.excel_parser import ExcelParser
from app.config import Config

class DataExtractor:
    """Extracts key CRE underwriting information from parsed documents"""
    
    def __init__(self, file_path: str, file_type: str, use_openai: Optional[bool] = None):
        self.file_path = file_path
        self.file_type = file_type
        self.use_openai = use_openai if use_openai is not None else Config.USE_OPENAI_EXTRACTION
        self.parser = self._get_parser()
        self.raw_data = {}
        self.extracted_metrics = {}
    
    def _get_parser(self):
        """Get appropriate parser based on file type"""
        if self.file_type.lower() == 'pdf':
            return PDFParser(self.file_path)
        elif self.file_type.lower() == 'word':
            return WordParser(self.file_path)
        elif self.file_type.lower() == 'excel':
            return ExcelParser(self.file_path)
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")
    
    def extract_all(self) -> Dict[str, Any]:
        """Extract all available information using OpenAI or regex-based methods"""
        self.raw_data = self.parser.parse()
        
        # Get text for extraction
        text = self.parser.extract_text()
        
        # Use OpenAI if enabled and configured
        if self.use_openai and Config.validate_openai_config():
            try:
                from app.parsers.openai_extractor import OpenAIExtractor
                openai_extractor = OpenAIExtractor()
                self.extracted_metrics = openai_extractor.extract_with_confidence(text)
                extraction_method = 'openai'
            except Exception as e:
                # Fallback to regex extraction if OpenAI fails and fallback is enabled
                if Config.ENABLE_FALLBACK:
                    self.extracted_metrics = self._extract_metrics_regex(text)
                    extraction_method = 'regex_fallback'
                else:
                    raise Exception(f"OpenAI extraction failed and fallback disabled: {str(e)}")
        else:
            # Use regex-based extraction
            self.extracted_metrics = self._extract_metrics_regex(text)
            extraction_method = 'regex'
        
        return {
            'file_info': {
                'file_type': self.file_type,
                'pages': self.raw_data.get('pages') or len(self.raw_data.get('sheets', [])),
                'file_path': self.file_path,
                'extraction_method': extraction_method
            },
            'raw_data': self.raw_data,
            'extracted_metrics': self.extracted_metrics
        }
    
    def _extract_metrics_regex(self, text: str) -> Dict[str, Any]:
        """Extract metrics using regex patterns with citation support"""
        return {
            'property_details': self._extract_property_details_with_citations(text),
            'financial_metrics': self._extract_financial_metrics_with_citations(text),
            'loan_details': self._extract_loan_details_with_citations(text),
            'tenant_information': {
                'major_tenants': self._find_multiple_patterns_with_citations(text, r'(?:Tenant|Anchor|Major Tenant):\s*([^\n]+)', 5),
                'lease_terms': self._find_pattern_with_citation(text, r'(?:Lease Term|Remaining Term):\s*([^\n]+)', 0),
                'tenant_quality': self._find_pattern_with_citation(text, r'(?:Tenant Quality|Credit Quality):\s*([^\n]+)', 0)
            },
            'market_analysis': self._extract_market_analysis_with_citations(text),
            'risk_assessment': {
                'identified_risks': self._find_multiple_patterns_with_citations(text, r'(?:Risk|Risk Factor|Concern):\s*([^\n]+)', 5),
                'mitigation_strategies': self._find_multiple_patterns_with_citations(text, r'(?:Mitigation|Mitigation Strategy):\s*([^\n]+)', 5)
            },
            'extraction_metadata': {
                'confidence_score': 0.0,
                'missing_fields': [],
                'fields_with_citations': 0,
                'fields_without_citations': 0,
                'citation_coverage_percent': 0.0
            }
        }
    
    def _extract_property_details(self, text: str) -> Dict[str, Optional[str]]:
        """Extract property details like address, type, size"""
        details = {
            'property_address': self._find_pattern(text, r'(?:Address|Location|Property):\s*([^\n]+)', 0),
            'property_type': self._find_pattern(text, r'(?:Property Type|Asset Class):\s*([^\n]+)', 0),
            'square_footage': self._find_pattern(text, r'(?:Square Feet|SF|Total Area):\s*([\d,]+)', 0),
            'year_built': self._find_pattern(text, r'(?:Year Built|Year Constructed):\s*(\d{4})', 0),
            'units': self._find_pattern(text, r'(?:Number of Units|Total Units):\s*(\d+)', 0),
            'occupancy_rate': self._find_pattern(text, r'(?:Occupancy Rate|Occupancy):\s*([\d.]+%)', 0)
        }
        return {k: v for k, v in details.items() if v}
    
    def _extract_property_details_with_citations(self, text: str) -> Dict[str, Any]:
        """Extract property details with source citations"""
        details = {
            'property_address': self._find_pattern_with_source(text, r'(?:Address|Location|Property):\s*([^\n]+)', 0),
            'property_type': self._find_pattern_with_source(text, r'(?:Property Type|Asset Class):\s*([^\n]+)', 0),
            'square_footage': self._find_pattern_with_source(text, r'(?:Square Feet|SF|Total Area):\s*([\d,]+)', 0),
            'acres': self._find_pattern_with_source(text, r'(?:Acres|Acreage|Land Area):\s*([\d,.]+)', 0),
            'land_square_feet': self._find_pattern_with_source(text, r'(?:Land Square Feet|Land SF|Land Area\s*\(SF\)):\s*([\d,]+)', 0),
            'gross_building_area': self._find_pattern_with_source(text, r'(?:Gross Building Area|GBA):\s*([\d,]+)', 0),
            'net_rentable_area': self._find_pattern_with_source(text, r'(?:Net Rentable Area|NRA):\s*([\d,]+)', 0),
            'year_built': self._find_pattern_with_source(text, r'(?:Year Built|Year Constructed):\s*(\d{4})', 0),
            'units': self._find_pattern_with_source(text, r'(?:Number of Units|Total Units):\s*(\d+)', 0),
            'occupancy_rate': self._find_pattern_with_source(text, r'(?:Occupancy Rate|Occupancy):\s*([\d.]+%)', 0)
        }
        return details
    
    def _extract_financial_metrics(self, text: str) -> Dict[str, Optional[str]]:
        """Extract financial metrics like NOI, cap rate, valuations"""
        metrics = {
            'noi_annual': self._find_pattern(text, r'(?:Net Operating Income|NOI):\s*\$?([\d,]+\.?\d*)', 0),
            'cap_rate': self._find_pattern(text, r'(?:Cap Rate|Capitalization Rate):\s*([\d.]+)%?', 0),
            'purchase_price': self._find_pattern(text, r'(?:Purchase Price|Acquisition Price):\s*\$?([\d,]+\.?\d*)', 0),
            'appraised_value': self._find_pattern(text, r'(?:Appraised Value|Valuation):\s*\$?([\d,]+\.?\d*)', 0),
            'annual_gross_income': self._find_pattern(text, r'(?:Gross Income|Annual Revenue):\s*\$?([\d,]+\.?\d*)', 0),
            'operating_expenses': self._find_pattern(text, r'(?:Operating Expenses|OpEx):\s*\$?([\d,]+\.?\d*)', 0),
            'debt_service': self._find_pattern(text, r'(?:Debt Service|Annual Debt Service):\s*\$?([\d,]+\.?\d*)', 0),
            'dscr': self._find_pattern(text, r'(?:DSCR|Debt Service Coverage Ratio):\s*([\d.]+)', 0),
            'irr': self._find_pattern(text, r'(?:IRR|Internal Rate of Return):\s*([\d.]+)%?', 0)
        }
        return {k: v for k, v in metrics.items() if v}
    
    def _extract_financial_metrics_with_citations(self, text: str) -> Dict[str, Any]:
        """Extract financial metrics with citations"""
        metrics = {
            'noi_annual': self._find_pattern_with_source(text, r'(?:Net Operating Income|NOI):\s*\$?([\d,]+\.?\d*)', 0),
            'stabilized_noi': self._find_pattern_with_source(text, r'(?:Stabilized NOI|Stabilized Net Operating Income):\s*\$?([\d,]+\.?\d*)', 0),
            'cap_rate': self._find_pattern_with_source(text, r'(?:Cap Rate|Capitalization Rate):\s*([\d.]+)%?', 0),
            'purchase_price': self._find_pattern_with_source(text, r'(?:Purchase Price|Acquisition Price):\s*\$?([\d,]+\.?\d*)', 0),
            'appraised_value': self._find_pattern_with_source(text, r'(?:Appraised Value|Valuation):\s*\$?([\d,]+\.?\d*)', 0),
            'annual_gross_income': self._find_pattern_with_source(text, r'(?:Gross Income|Annual Revenue):\s*\$?([\d,]+\.?\d*)', 0),
            'operating_expenses': self._find_pattern_with_source(text, r'(?:Operating Expenses|OpEx):\s*\$?([\d,]+\.?\d*)', 0),
            'debt_service': self._find_pattern_with_source(text, r'(?:Debt Service|Annual Debt Service):\s*\$?([\d,]+\.?\d*)', 0),
            'dscr': self._find_pattern_with_source(text, r'(?:DSCR|Debt Service Coverage Ratio):\s*([\d.]+)', 0),
            'irr': self._find_pattern_with_source(text, r'(?:IRR|Internal Rate of Return):\s*([\d.]+)%?', 0),
            'project_cost': self._find_pattern_with_source(text, r'(?:Total Project Cost|Project Cost|Total Cost):\s*\$?([\d,]+\.?\d*)', 0),
            'expected_exit_valuation': self._find_pattern_with_source(text, r'(?:Expected Exit Valuation|Exit Valuation|Terminal Value):\s*\$?([\d,]+\.?\d*)', 0),
            'expected_rents': []
        }
        return metrics
    
    def _extract_loan_details(self, text: str) -> Dict[str, Optional[str]]:
        """Extract loan terms and conditions"""
        details = {
            'loan_amount': self._find_pattern(text, r'(?:Loan Amount|Credit Facility):\s*\$?([\d,]+\.?\d*)', 0),
            'interest_rate': self._find_pattern(text, r'(?:Interest Rate|Rate):\s*([\d.]+)%?', 0),
            'loan_term_years': self._find_pattern(text, r'(?:Loan Term|Amortization Period):\s*(\d+)\s*(?:year|month)', 0),
            'loan_type': self._find_pattern(text, r'(?:Loan Type|Facility Type):\s*([^\n]+)', 0),
            'lender': self._find_pattern(text, r'(?:Lender|Bank|Financial Institution):\s*([^\n]+)', 0),
            'maturity_date': self._find_pattern(text, r'(?:Maturity Date|Loan Maturity):\s*([^\n]+)', 0),
            'ltv': self._find_pattern(text, r'(?:LTV|Loan to Value):\s*([\d.]+)%?', 0)
        }
        return {k: v for k, v in details.items() if v}
    
    def _extract_loan_details_with_citations(self, text: str) -> Dict[str, Any]:
        """Extract loan details with citations"""
        details = {
            'loan_amount': self._find_pattern_with_source(text, r'(?:Loan Amount|Credit Facility):\s*\$?([\d,]+\.?\d*)', 0),
            'interest_rate': self._find_pattern_with_source(text, r'(?:Interest Rate|Rate):\s*([\d.]+)%?', 0),
            'loan_term_years': self._find_pattern_with_source(text, r'(?:Loan Term|Amortization Period):\s*(\d+)\s*(?:year|month)', 0),
            'loan_type': self._find_pattern_with_source(text, r'(?:Loan Type|Facility Type):\s*([^\n]+)', 0),
            'lender': self._find_pattern_with_source(text, r'(?:Lender|Bank|Financial Institution):\s*([^\n]+)', 0),
            'maturity_date': self._find_pattern_with_source(text, r'(?:Maturity Date|Loan Maturity):\s*([^\n]+)', 0),
            'ltv': self._find_pattern_with_source(text, r'(?:LTV|Loan to Value):\s*([\d.]+)%?', 0)
        }
        return details
    
    def _extract_market_analysis(self, text: str) -> Dict[str, Any]:
        """Extract market-related information"""
        analysis = {
            'market': self._find_pattern(text, r'(?:Market|Market Analysis|MSA):\s*([^\n]+)', 0),
            'submarket': self._find_pattern(text, r'(?:Submarket|Sub-market):\s*([^\n]+)', 0),
            'comparable_properties': self._find_multiple_patterns(text, r'(?:Comparable|Comp|Similar Properties):\s*([^\n]+)', 5),
            'market_trends': self._find_multiple_patterns(text, r'(?:Market Trend|Trend):\s*([^\n]+)', 5)
        }
        return {k: v for k, v in analysis.items() if v}
    
    def _extract_market_analysis_with_citations(self, text: str) -> Dict[str, Any]:
        """Extract market analysis with citations"""
        analysis = {
            'market': self._find_pattern_with_source(text, r'(?:Market|Market Analysis|MSA):\s*([^\n]+)', 0),
            'submarket': self._find_pattern_with_source(text, r'(?:Submarket|Sub-market):\s*([^\n]+)', 0),
            'comparable_properties': self._find_multiple_patterns_with_sources(text, r'(?:Comparable|Comp|Similar Properties):\s*([^\n]+)', 5),
            'market_trends': self._find_multiple_patterns_with_sources(text, r'(?:Market Trend|Trend):\s*([^\n]+)', 5)
        }
        return analysis
    
    def _find_pattern(self, text: str, pattern: str, index: int = 0) -> Optional[str]:
        """Find a single pattern in text"""
        try:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            return matches[index] if matches and index < len(matches) else None
        except:
            return None
    
    def _find_multiple_patterns(self, text: str, pattern: str, limit: int = 5) -> List[str]:
        """Find multiple patterns in text"""
        try:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            return [m.strip() for m in matches[:limit] if m.strip()]
        except:
            return []
    
    def _find_pattern_with_citation(self, text: str, pattern: str, index: int = 0) -> Dict[str, Optional[str]]:
        """Find a single pattern in text and return with citation"""
        try:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            match_list = list(matches)
            
            if match_list and index < len(match_list):
                match = match_list[index]
                value = match.group(1).strip() if match.lastindex and match.lastindex >= 1 else None
                
                if value:
                    # Get surrounding context for source text (up to 100 chars before and after)
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    source_text = text[start:end].strip()
                    
                    return {"value": value, "unit": None, "source_text": source_text}
            
            return {"value": None, "unit": None, "source_text": None}
        except:
            return {"value": None, "unit": None, "source_text": None}
    
    def _find_multiple_patterns_with_citations(self, text: str, pattern: str, limit: int = 5) -> List[Dict[str, Optional[str]]]:
        """Find multiple patterns in text with citations"""
        try:
            matches = list(re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE))
            results = []
            
            for match in matches[:limit]:
                value = match.group(1).strip() if match.lastindex and match.lastindex >= 1 else None
                
                if value:
                    # Get surrounding context for citation
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    source_text = text[start:end].strip()
                    
                    if "tenant" in pattern.lower():
                        key = "name"
                    elif "risk" in pattern.lower():
                        key = "risk"
                    elif "mitigation" in pattern.lower() or "strategy" in pattern.lower():
                        key = "strategy"
                    elif "trend" in pattern.lower():
                        key = "trend"
                    else:
                        key = "property"

                    results.append({
                        key: value,
                        "source_text": source_text
                    })
            
            return results
        except:
            return []

    def _find_pattern_with_source(self, text: str, pattern: str, index: int = 0) -> Dict[str, Optional[str]]:
        """Find a single pattern in text and return with source_text"""
        return self._find_pattern_with_citation(text, pattern, index)

    def _find_multiple_patterns_with_sources(self, text: str, pattern: str, limit: int = 5) -> List[Dict[str, Optional[str]]]:
        """Find multiple patterns in text with source_text"""
        return self._find_multiple_patterns_with_citations(text, pattern, limit)

