from abc import ABC, abstractmethod
from typing import Any
from ragnarok.models import DocumentIIR

class BaseParser(ABC):
    """Base interface for all document parsers."""
    
    @abstractmethod
    def parse(self, file_path: str, **kwargs: Any) -> DocumentIIR:
        """
        Parse the input file into the standard DocumentIIR format.
        
        Args:
            file_path: Path to the document.
            **kwargs: Additional parsing options.
            
        Returns:
            DocumentIIR: The parsed structural representation.
        """
        pass
