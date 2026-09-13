from abc import ABC, abstractmethod

from radar.domain import RawEventObservation


class ExtractionStrategy(ABC):
    @abstractmethod
    def extract(self, document: str, source_url: str) -> list[RawEventObservation]:
        raise NotImplementedError
