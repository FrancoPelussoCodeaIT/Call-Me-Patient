from abc import ABC, abstractmethod
from collections import Counter
from typing import List

from call_me_patient.models import PatientInfo


class WranglerMixin(ABC):
    @abstractmethod
    def wrangle(self, info: List[PatientInfo], *args, **kwargs) -> PatientInfo:
        """This method will take all differing data for a patient and return the definitive's."""

    def __call__(self, info: List[PatientInfo], *args, **kwargs):
        return self.wrangle(info, *args, **kwargs)


class MostRepeatedWrangler(WranglerMixin):
    def wrangle(self, info: List[PatientInfo], allow_ties: bool = False) -> PatientInfo:
        counters = (Counter(), Counter(), Counter())
        for data in info:
            counters[0].update([data.deductible])
            counters[1].update([data.stop_loss])
            counters[2].update([data.oop_max])
        return PatientInfo({
            'deductible': self._get_wrangled_field_from_top(
                counters[0].most_common(2), allow_ties
            ),
            'stop_loss': self._get_wrangled_field_from_top(counters[1].most_common(2), allow_ties),
            'oop_max': self._get_wrangled_field_from_top(counters[2].most_common(2), allow_ties)
        })

    def _get_wrangled_field_from_top(self, field_tops: List[tuple], allow_ties: bool = False):
        if len(field_tops) > 1 and field_tops[0][1] == field_tops[1][1] and not allow_ties:
            return None
        return field_tops[0][0]


class AverageWrangler(WranglerMixin):
    def wrangle(self, info: List[PatientInfo], allow_ties: bool = False) -> PatientInfo:
        total_count = len(info)
        sums = [0, 0, 0]
        for data in info:
            sums[0] += data.deductible
            sums[1] += data.stop_loss
            sums[2] += data.oop_max
        return PatientInfo({
            'deductible': round(sums[0] / total_count),
            'stop_loss': round(sums[1] / total_count),
            'oop_max': round(sums[2] / total_count)
        })
