from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseParser(ABC):
    """Base class for document parsers"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.extracted_data = {}
    
    @abstractmethod
    def parse(self) -> Dict[str, Any]:
        """Parse the document and extract data"""
        pass
    
    @abstractmethod
    def extract_text(self) -> str:
        """Extract all text from the document"""
        pass
    
    def get_extracted_data(self) -> Dict[str, Any]:
        """Return extracted data"""
        return self.extracted_data
