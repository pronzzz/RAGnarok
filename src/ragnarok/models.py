from dataclasses import dataclass, field
from typing import List, Optional, Any

@dataclass
class Block:
    """Base class for any layout block in the document."""
    text: str

@dataclass
class Paragraph(Block):
    pass

@dataclass
class Heading(Block):
    level: int

@dataclass
class TableRow:
    cells: List[str]

@dataclass
class Table(Block):
    rows: List[TableRow]

@dataclass
class ConfidenceScore:
    overall: float = 1.0
    ocr: float = 1.0
    layout: float = 1.0
    table: float = 1.0

@dataclass
class Page:
    page_number: int
    blocks: List[Block] = field(default_factory=list)
    confidence: ConfidenceScore = field(default_factory=ConfidenceScore)
    is_corrupted: bool = False
    
@dataclass
class DocumentIIR:
    pages: List[Page] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
