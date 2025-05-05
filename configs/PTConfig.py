import sys
sys.path.insert(0,r'./')

from .config import Config
from typing import List, Dict
from dataclasses import dataclass, asdict, fields


@dataclass
class PTConfig(Config):

    hu_prompt: str = None
    hu_text: str = None
    corpus_lengths: int = None

    def __post_init__(self) -> None:
        # Post validate
        self.corpus_lengths = len(self.hu_prompt) + len(self.hu_txt) if (self.hu_prompt is not None and self.hu_text) else None

    @property
    def __repr__(self) -> str:
        '''
        s = ""
        s += f"\n Text id: {self.qas_id}"
        if self.orig_corpus_texts:
            s += f"\n Text: {self.orig_corpus_texts}"
            s += f"\n Length: {self.corpus_lengths}"
        '''
        return f'Text: {self.hu_prompt} \n {self.hu_text}'

    @property
    def get_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def get_keys(self) -> List[str]:
        all_fields = fields(self)
        return [v.name for v in all_fields]
