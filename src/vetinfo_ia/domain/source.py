from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    document: str
    page: int
    excerpt: str
