import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

from call_me_patient.models import Patient, PatientInfo
from call_me_patient.parsers import DictListParserMixin, JSONParserMixin, ParserMixin
from call_me_patient.wranglers import MostRepeatedWrangler, WranglerMixin


@dataclass
class PatientQuery(ParserMixin, ABC):
    wranglers: List[WranglerMixin] = field(default_factory=lambda: [MostRepeatedWrangler()])

    @abstractmethod
    def get_info(self, member_data):
        """This method will read information needed given a certain member data, i.e. its id.""" 

    def get_parsed_info(self, member_data = None) -> PatientInfo:
        return self.parse(self.get_info(member_data))

    def get_full_patient_info(self, member_data = None, *args, **kwargs) -> Patient:
        return Patient({
            'member_id': self._get_member_id(member_data),
            'info': self.wrangle(self.get_parsed_info(member_data), *args, **kwargs)
        })

    def _get_member_id(self, member_data = None) -> int:
        return member_data

    def wrangle(self, info: List[PatientInfo], *args, **kwargs) -> PatientInfo:
        wrangled_info = PatientInfo()
        wranglers = iter(self.wranglers)
        wrangler = next(wranglers, None)
        while wrangler is not None and not wrangled_info.is_filled():
            wrangled_info.update(wrangler(info, *args, **kwargs))
            wrangler = next(wranglers, None)
        return wrangled_info


@dataclass
class DummyPatientQuery(DictListParserMixin, PatientQuery):
    dummy_data: dict = field(default_factory=lambda: {
        1: [
            {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000},
            {'deductible': 1200, 'stop_loss': 13000, 'oop_max': 6000},
            {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 6000}
        ]
    })

    def get_info(self, member_id: int = None):
        info = self.dummy_data.get(member_id) or next(iter(self.dummy_data.values()))
        return info


@dataclass
class JSONFilePatientQuery(DictListParserMixin, PatientQuery):
    filename: str = 'example_data.json'

    def get_info(self, member_id: int):
        info_db = self._get_infodb()
        return info_db.get(str(member_id)) or next(iter(self._infodb.values()))

    def _get_infodb(self) -> dict:
        if getattr(self, '_infodb', None) is None:
            with open(self.filename, 'r') as info_file:
                self._infodb = json.load(info_file)
        return self._infodb
