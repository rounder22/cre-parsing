import pdfplumber
from typing import Dict, Any, List
from app.parsers.base_parser import BaseParser

class PDFParser(BaseParser):
    """Parser for PDF documents"""
    
    def parse(self) -> Dict[str, Any]:
        """Parse PDF and extract structured data"""
        try:
            with pdfplumber.open(self.file_path) as pdf:
                self.extracted_data = {
                    'file_type': 'PDF',
                    'pages': len(pdf.pages),
                    'text': self._extract_all_text(pdf),
                    'tables': self._extract_tables(pdf),
                    'metadata': pdf.metadata or {}
                }
            return self.extracted_data
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    def extract_text(self) -> str:
        """Extract all text from PDF"""
        try:
            with pdfplumber.open(self.file_path) as pdf:
                return self._extract_all_text(pdf)
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def _extract_all_text(self, pdf) -> str:
        """Extract text from all pages"""
        text = ""
        for page_num, page in enumerate(pdf.pages, 1):
            text += f"\n--- PAGE {page_num} ---\n"
            text += page.extract_text() or ""
        return text
    
    def _extract_tables(self, pdf) -> List[List[Dict]]:
        """Extract tables from PDF"""
        tables = []
        for page_num, page in enumerate(pdf.pages, 1):
            page_tables = page.extract_tables()
            if page_tables:
                for table in page_tables:
                    tables.append({
                        'page': page_num,
                        'data': table
                    })
        return tables
