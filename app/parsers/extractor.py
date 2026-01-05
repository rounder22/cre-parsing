import re
from typing import Dict, Any, List, Optional
from app.parsers.pdf_parser import PDFParser
from app.parsers.word_parser import WordParser
from app.parsers.excel_parser import ExcelParser

class DataExtractor:
    """Extracts key CRE underwriting information from parsed documents"""
    
    def __init__(self, file_path: str, file_type: str):
        self.file_path = file_path
        self.file_type = file_type
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
        """Extract all available information"""
        self.raw_data = self.parser.parse()
        
        # Get text for keyword extraction
        text = self.parser.extract_text()
        
        # Extract CRE-specific metrics
        self.extracted_metrics = {
            'property_details': self._extract_property_details(text),
            'financial_metrics': self._extract_financial_metrics(text),
            'loan_details': self._extract_loan_details(text),
            'tenant_info': self._extract_tenant_info(text),
            'market_analysis': self._extract_market_analysis(text),
            'risk_factors': self._extract_risk_factors(text)
        }
        
        return {
            'file_info': {
                'file_type': self.file_type,
                'pages': self.raw_data.get('pages') or len(self.raw_data.get('sheets', [])),
                'file_path': self.file_path
            },
            'raw_data': self.raw_data,
            'extracted_metrics': self.extracted_metrics
        }
    
    def _extract_property_details(self, text: str) -> Dict[str, Optional[str]]:
        """Extract property details like address, type, size"""
        details = {
            'property_address': self._find_pattern(text, r'(?:Address|Location|Property):\s*([^\n]+)', 0),
            'property_type': self._find_pattern(text, r'(?:Property Type|Asset Class):\s*([^\n]+)', 0),
            'square_footage': self._find_pattern(text, r'(?:Square Feet|SF|Total Area):\s*([\d,]+)', 0),
            'year_built': self._find_pattern(text, r'(?:Year Built|Year Constructed):\s*(\d{4})', 0),
            'units': self._find_pattern(text, r'(?:Number of Units|Total Units):\s*(\d+)', 0),
            'occupancy': self._find_pattern(text, r'(?:Occupancy Rate|Occupancy):\s*([\d.]+%)', 0)
        }
        return {k: v for k, v in details.items() if v}
    
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
    
    def _extract_loan_details(self, text: str) -> Dict[str, Optional[str]]:
        """Extract loan terms and conditions"""
        details = {
            'loan_amount': self._find_pattern(text, r'(?:Loan Amount|Credit Facility):\s*\$?([\d,]+\.?\d*)', 0),
            'interest_rate': self._find_pattern(text, r'(?:Interest Rate|Rate):\s*([\d.]+)%?', 0),
            'loan_term': self._find_pattern(text, r'(?:Loan Term|Amortization Period):\s*(\d+)\s*(?:year|month)', 0),
            'loan_type': self._find_pattern(text, r'(?:Loan Type|Facility Type):\s*([^\n]+)', 0),
            'lender': self._find_pattern(text, r'(?:Lender|Bank|Financial Institution):\s*([^\n]+)', 0),
            'maturity_date': self._find_pattern(text, r'(?:Maturity Date|Loan Maturity):\s*([^\n]+)', 0),
            'ltv': self._find_pattern(text, r'(?:LTV|Loan to Value):\s*([\d.]+)%?', 0)
        }
        return {k: v for k, v in details.items() if v}
    
    def _extract_tenant_info(self, text: str) -> Dict[str, Optional[str]]:
        """Extract tenant and tenant mix information"""
        info = {
            'major_tenants': self._find_multiple_patterns(text, r'(?:Tenant|Anchor|Major Tenant):\s*([^\n]+)', 3),
            'lease_terms': self._find_pattern(text, r'(?:Lease Term|Remaining Term):\s*([^\n]+)', 0),
            'tenant_quality': self._find_pattern(text, r'(?:Tenant Quality|Credit Quality):\s*([^\n]+)', 0)
        }
        return {k: v for k, v in info.items() if v}
    
    def _extract_market_analysis(self, text: str) -> Dict[str, Optional[str]]:
        """Extract market-related information"""
        analysis = {
            'market': self._find_pattern(text, r'(?:Market|Market Analysis|MSA):\s*([^\n]+)', 0),
            'submarket': self._find_pattern(text, r'(?:Submarket|Sub-market):\s*([^\n]+)', 0),
            'comparable_properties': self._find_pattern(text, r'(?:Comparable|Comp|Similar Properties):\s*([^\n]+)', 0),
            'market_trends': self._find_pattern(text, r'(?:Market Trend|Trend):\s*([^\n]+)', 0)
        }
        return {k: v for k, v in analysis.items() if v}
    
    def _extract_risk_factors(self, text: str) -> Dict[str, Optional[str]]:
        """Extract risk factors and considerations"""
        factors = {
            'risks': self._find_multiple_patterns(text, r'(?:Risk|Risk Factor|Concern):\s*([^\n]+)', 5),
            'mitigation': self._find_pattern(text, r'(?:Mitigation|Mitigation Strategy):\s*([^\n]+)', 0)
        }
        return {k: v for k, v in factors.items() if v}
    
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
