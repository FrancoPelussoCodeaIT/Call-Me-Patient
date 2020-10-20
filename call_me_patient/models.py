from schematics.models import Model
from schematics.types import StringType, IntType, ModelType


class PatientInfo(Model):
    deductible = IntType()
    stop_loss = IntType()
    oop_max = IntType()

    def is_filled(self) -> bool:
        return all([
            self.deductible is not None,
            self.stop_loss is not None,
            self.oop_max is not None
        ])

    def update(self, updated_fields, force: bool = False):
        for field in self._fields.keys():  # pylint: disable=no-member
            updated = getattr(updated_fields, field, None)
            must_update = getattr(self, field, None) is None or force
            if updated and must_update:
                setattr(self, field, updated)                

    def __repr__(self):
        return (
            f'PatientInfo(deductible={self.deductible}, stop_loss={self.stop_loss}, '
            f'oop_max={self.oop_max})'
        )


class Patient(Model):
    member_id = IntType(required=True)
    info = ModelType(PatientInfo, required=False)

    def __repr__(self):
        return f'Patient(member_id={self.member_id}, info={self.info})'
