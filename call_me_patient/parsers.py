import json
from abc import ABC, abstractmethod
from typing import List

from call_me_patient.models import PatientInfo


class ParserMixin(ABC):
    @abstractmethod
    def parse(self, info) -> PatientInfo:
        """This could take a different input depending on the source but always return the same
        structure."""


class JSONParserMixin(ParserMixin):
    def parse(self, info: str) -> PatientInfo:
        input_info = json.loads(info) if info else {}
        return PatientInfo(input_info)


class DictListParserMixin(ParserMixin):
    def parse(self, info: List[dict]) -> PatientInfo:
        return [PatientInfo(i) for i in info]
