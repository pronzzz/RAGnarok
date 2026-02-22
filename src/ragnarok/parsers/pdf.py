import pdfplumber
from typing import Any
import logging

from ragnarok.parsers.base import BaseParser
from ragnarok.models import DocumentIIR, Page, Paragraph, Table, TableRow

logger = logging.getLogger("ragnarok")

class PDFParser(BaseParser):
    """Standard baseline parser for PDF documents using pdfplumber."""
    
    def parse(self, file_path: str, **kwargs: Any) -> DocumentIIR:
        doc_iir = DocumentIIR()
        
        try:
            with pdfplumber.open(file_path) as pdf:
                doc_iir.metadata = pdf.metadata or {}
                
                for i, pdf_page in enumerate(pdf.pages):
                    page_iir = Page(page_number=i + 1)
                    
                    # Extract tables first
                    tables = pdf_page.extract_tables()
                    
                    # Baseline text extraction (ignores structural layout complexities for Phase 2)
                    text = pdf_page.extract_text()
                    if text:
                        page_iir.blocks.append(Paragraph(text=text))
                    
                    # Append tables if any
                    for table_data in tables:
                        if not table_data:
                            continue
                        rows = []
                        for r in table_data:
                            # Clean up None cells
                            cells = [str(cell).replace('\n', ' ') if cell else "" for cell in r]
                            rows.append(TableRow(cells=cells))
                        if rows:
                            page_iir.blocks.append(Table(text="", rows=rows))

                    doc_iir.pages.append(page_iir)
        except Exception as e:
            logger.error(f"Failed to parse PDF {file_path}: {e}")
            raise
            
        return doc_iir
