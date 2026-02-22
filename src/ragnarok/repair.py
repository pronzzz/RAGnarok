import logging
import requests
from typing import Optional

from ragnarok.models import DocumentIIR, Page, Paragraph

logger = logging.getLogger("ragnarok")

class VLMRepairAgent:
    """Optional VLM interface to attempt repair on corrupted pages."""
    
    def __init__(self, ollama_url: str = "http://localhost:11434/api/generate", model: str = "llava"):
        self.ollama_url = ollama_url
        self.model = model
        self.is_available = self._check_availability()
        
    def _check_availability(self) -> bool:
        """Check if the local Ollama instance is running."""
        try:
            # We just do a dummy request to check if the server is alive
            response = requests.get(self.ollama_url.replace("/api/generate", ""), timeout=1)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            logger.warning("Local VLM (Ollama) not detected. Repair steps will be skipped.")
            return False

    def heal(self, doc_iir: DocumentIIR) -> DocumentIIR:
        """Attempt to heal all corrupted pages in the document."""
        if not self.is_available:
            return doc_iir
            
        for page in doc_iir.pages:
            if page.is_corrupted:
                logger.info(f"Attempting VLM repair on corrupted page {page.page_number}...")
                self._repair_page(page)
                
        return doc_iir
        
    def _repair_page(self, page: Page):
        """Send page content to VLM for structural repair (Simulated for text; requires image/LLaVA ideally)."""
        # In a full implementation, you'd convert the page to an image and send it to LLaVA.
        # Here we just send the garbled text and ask for reconstruction as an example hook.
        text_content = "\n".join(b.text for b in page.blocks if hasattr(b, "text"))
        
        prompt = (
            "You are a document reconstruction expert. Repair the following garbled text into "
            "clean markdown while preserving tables, headings, and logical structure:\n\n"
            f"{text_content}"
        )
        
        try:
            response = requests.post(
                self.ollama_url,
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=30
            )
            response.raise_for_status()
            repaired_text = response.json().get("response", "").strip()
            
            if repaired_text:
                # Replace the old blocks with the repaired single paragraph block (or parsed markdown logic)
                logger.info(f"VLM successfully repaired page {page.page_number}.")
                page.blocks = [Paragraph(text=repaired_text)]
                page.is_corrupted = False
                page.confidence.overall = 0.9  # Confident after VLM repair
        except Exception as e:
            logger.error(f"VLM repair failed on page {page.page_number}: {e}")
