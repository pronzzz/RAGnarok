import logging
from typing import List, Dict, Any
import json

from ragnarok.models import DocumentIIR, Page, Paragraph, Heading, Table

logger = logging.getLogger("ragnarok")

class RAGChunker:
    """Optimizes DocumentIIR into semantic chunks for RAG."""
    
    def __init__(self, max_tokens: int = 1000):
        # A rough heuristic: 1 word is ~1.3 tokens
        self.max_tokens = max_tokens
        
    def chunk(self, doc_iir: DocumentIIR) -> str:
        """Converts the IIR directly into a stream of RAG-optimized Markdown chunks."""
        chunks = []
        current_chunk = []
        current_tokens = 0
        current_headings = []
        
        for page in doc_iir.pages:
            for block in page.blocks:
                block_md = ""
                block_tokens = 0
                
                if isinstance(block, Heading):
                    block_md = f"{'#' * block.level} {block.text}\n\n"
                    # Update local hierarchy state
                    current_headings = current_headings[:block.level - 1] + [block.text]
                    
                elif isinstance(block, Paragraph):
                    block_md = f"{block.text}\n\n"
                    
                elif isinstance(block, Table):
                    if block.rows:
                        headers = block.rows[0].cells
                        block_md += "| " + " | ".join(headers) + " |\n"
                        block_md += "|" + "|".join(["---"] * len(headers)) + "|\n"
                        for row in block.rows[1:]:
                            block_md += "| " + " | ".join(row.cells) + " |\n"
                    block_md += "\n"
                    
                block_tokens = len(block_md.split()) * 1.3
                
                if current_tokens + block_tokens > self.max_tokens and current_chunk:
                    # Flush current chunk
                    chunks.append(self._finalize_chunk(current_chunk, current_headings, page.page_number))
                    current_chunk = []
                    current_tokens = 0
                    
                current_chunk.append(block_md)
                current_tokens += block_tokens
                
        if current_chunk:
            chunks.append(self._finalize_chunk(current_chunk, current_headings, doc_iir.pages[-1].page_number if doc_iir.pages else 1))
            
        return "\n\n---\n\n".join(chunks)
        
    def _finalize_chunk(self, blocks: List[str], hierarchy: List[str], page_num: int) -> str:
        """Adds semantic metadata to the top of a Markdown chunk."""
        meta = {
            "page": page_num,
            "hierarchy": " > ".join(hierarchy)
        }
        meta_md = f"<!-- RAG METADATA: {json.dumps(meta)} -->\n"
        return meta_md + "".join(blocks)
