from dataclasses import dataclass

from app.data.models import Candle


@dataclass
class DataQualityReport:
    candle_count: int
    gaps: list[tuple[Candle, Candle]]

    @property
    def has_gaps(self) -> bool:
        return len(self.gaps) > 0