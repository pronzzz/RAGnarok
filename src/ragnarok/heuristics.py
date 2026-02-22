import logging
import re
from typing import List

from ragnarok.models import DocumentIIR, Page, Paragraph

logger = logging.getLogger("ragnarok")

class DocumentValidator:
    """Heuristic logic to evaluate the structural integrity of parsed pages."""
    
    def validate(self, doc_iir: DocumentIIR) -> DocumentIIR:
        """Evaluate page confidences and flag corrupted pages."""
        for page in doc_iir.pages:
            self._evaluate_page(page)
            if page.confidence.overall < 0.7:
                page.is_corrupted = True
                logger.warning(f"Page {page.page_number} flagged as corrupted (Score: {page.confidence.overall:.2f}).")
        return doc_iir
        
    def _evaluate_page(self, page: Page):
        """Run heuristics on a single page to determine confidence score."""
        text_blocks = [b for b in page.blocks if isinstance(b, Paragraph)]
        if not text_blocks:
            page.confidence.overall = 1.0
            return
            
        full_text = "\n".join(b.text for b in text_blocks)
        
        # Heuristic 1: Garbled / OCR failure (High non-alphanumeric ratio)
        alpha_chars = sum(c.isalnum() for c in full_text)
        if len(full_text) > 50 and alpha_chars / len(full_text) < 0.5:
            page.confidence.ocr = 0.4
            
        # Heuristic 2: Column drift / broken wraps (many short lines)
        lines = full_text.split("\n")
        short_lines = sum(1 for line in lines if 0 < len(line.strip()) < 30)
        total_lines = max(1, len(lines))
        if total_lines > 10 and (short_lines / total_lines) > 0.6:
            page.confidence.layout = 0.5
            
        # Overall is the minimum of heuristic scores
        page.confidence.overall = min(page.confidence.ocr, page.confidence.layout, page.confidence.table)
