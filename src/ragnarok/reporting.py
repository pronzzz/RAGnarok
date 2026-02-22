import json
from typing import Dict, Any

from ragnarok.models import DocumentIIR

class Reporter:
    """Generates confidence and execution reporting."""
    
    def generate_report(self, doc_iir: DocumentIIR) -> Dict[str, Any]:
        """Convert document execution metadata and scores into a JSON-serializable report."""
        total_pages = len(doc_iir.pages)
        corrupted_pages = sum(1 for p in doc_iir.pages if p.is_corrupted)
        
        avg_confidence = (
            sum(p.confidence.overall for p in doc_iir.pages) / total_pages 
            if total_pages > 0 else 1.0
        )
        
        page_details = []
        for page in doc_iir.pages:
            page_details.append({
                "page": page.page_number,
                "corrupted": page.is_corrupted,
                "scores": {
                    "overall": round(page.confidence.overall, 2),
                    "ocr": round(page.confidence.ocr, 2),
                    "layout": round(page.confidence.layout, 2),
                    "table": round(page.confidence.table, 2)
                }
            })
            
        report = {
            "summary": {
                "total_pages": total_pages,
                "corrupted_pages": corrupted_pages,
                "average_confidence": round(avg_confidence, 2)
            },
            "pages": page_details,
            "metadata": doc_iir.metadata
        }
        
        return report
