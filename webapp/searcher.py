from dataclasses import dataclass
from typing import Optional


@dataclass
class Waterfall:
    uid: int
    title: str


class WaterfallSearcher:
    bear = Waterfall(uid=1, title='Медвежий водопад')
    niagara = Waterfall(uid=2, title='Ниагарский водопад')

    model = {
        'медведь': bear,
        'медвежий': bear,
        'про мишек': bear,
        'ниагара': niagara,
    }

    def search(self, text: str) -> Optional[Waterfall]:
        words = text.lower().split()
        for word in words:
            if word in self.model:
                return self.model[word]

        return None
