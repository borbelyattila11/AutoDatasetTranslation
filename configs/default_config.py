import sys

from .config import Config
from typing import List, Dict
from dataclasses import dataclass, asdict, fields

@dataclass
class DefaultConfig(Config):

    hu_caps: str = None
    corpus_lengths: int = None

    def __post_init__(self) -> None:
        self.corpus_lengths = len(self.hu_caps) if self.hu_caps is not None else None

    @property
    def __repr__(self) -> str:
        return f'Text: {self.hu_caps}'

    @property
    def get_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def get_keys(cls) -> List[str]:
        all_fields = fields(cls)
        return [ v.name for v in all_fields ]
