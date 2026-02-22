import os
import logging
from typing import Optional

from ragnarok.models import DocumentIIR, Paragraph, Table, Heading
from ragnarok.parsers.pdf import PDFParser

logger = logging.getLogger("ragnarok")

class Orchestrator:
    """Coordinates document parsing, validation, and generation."""
    
    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        
    def process(self, file_path: str) -> tuple[str, "DocumentIIR"]:
        """
        Process the document and return Markdown string and DocumentIIR.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        ext = os.path.splitext(file_path)[1].lower()
        
        parser = None
        if ext == ".pdf":
            parser = PDFParser()
        else:
            raise ValueError(f"Unsupported file format: {ext}")
            
        logger.info(f"Parsing {file_path} using {parser.__class__.__name__}...")
        doc_iir = parser.parse(file_path)
        
        from ragnarok.heuristics import DocumentValidator
        validator = DocumentValidator()
        doc_iir = validator.validate(doc_iir)
        
        corrupted = sum(1 for p in doc_iir.pages if p.is_corrupted)
        logger.info(f"Parsed {len(doc_iir.pages)} pages successfully. Detected {corrupted} corrupted pages.")
        
        if corrupted > 0:
            from ragnarok.repair import VLMRepairAgent
            repair_agent = VLMRepairAgent()
            doc_iir = repair_agent.heal(doc_iir)
            
            # Recalculate remaining corrupted pages
            corrupted_after = sum(1 for p in doc_iir.pages if p.is_corrupted)
            logger.info(f"Repair attempt complete. Pages still corrupted: {corrupted_after}")
        
        # Generate RAG Optimized Markdown Chunks
        from ragnarok.chunking import RAGChunker
        chunker = RAGChunker(max_tokens=self.config.get("chunk_size", 1000))
        markdown = chunker.chunk(doc_iir)
        
        return markdown, doc_iir
