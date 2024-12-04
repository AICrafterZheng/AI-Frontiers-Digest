from dataclasses import dataclass
from datetime import datetime

@dataclass
class Story:
    id: int = 0
    title: str = ""
    url: str = ""
    score: int = 0
    hn_url: str = ""
    summary: str = ""
    comments_summary: str = ""
    source: str = ""
    content: str = ""
    speech_url: str = ""
    notebooklm_url: str = ""

@dataclass
class Comment:
    id: int
    text: str
    author: str
    created_at: datetime