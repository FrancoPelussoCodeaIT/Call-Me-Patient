import json
import unittest

from call_me_patient.models import Patient, PatientInfo
from call_me_patient.parsers import DictListParserMixin, JSONParserMixin
from call_me_patient.patients import DummyPatientQuery, JSONFilePatientQuery
from call_me_patient.wranglers import AverageWrangler, MostRepeatedWrangler


EXAMPLE_PATIENT_JSON_FILENAME = 'example_data.json'


class AssertResultTestCase(unittest.TestCase):
    def _assert_result(self, result, expected):
        self.assertEqual(result, expected)


class ParsersTest(AssertResultTestCase):
    DICT_LIST_PARSER = DictListParserMixin()
    JSON_PARSER = JSONParserMixin()

    def test_dict_list_parser_empty(self):
        self._assert_result(
            result=self.DICT_LIST_PARSER.parse([]),
            expected=[]
        )

    def test_dict_list_parser_single(self):

        patient_data = {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000}
        self._assert_result(
            result=self.DICT_LIST_PARSER.parse([patient_data]),
            expected=[PatientInfo(patient_data)]
        )

    def test_dict_list_parser_many(self):
        patients_data = [
            {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000},
            {'deductible': 1200, 'stop_loss': 13000, 'oop_max': 6000},
            {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 6000}
        ]
        self._assert_result(
            result=self.DICT_LIST_PARSER.parse(patients_data),
            expected=[PatientInfo(data) for data in patients_data]
        )

    def test_json_parser_empty(self):
        self._assert_result(
            result=self.JSON_PARSER.parse(""),
            expected=PatientInfo({})
        )

    def test_json_parser_one(self):

        patient_data = """{"deductible": 1000, "stop_loss": 10000, "oop_max": 5000}"""
        self._assert_result(
            result=self.JSON_PARSER.parse(patient_data),
            expected=PatientInfo(json.loads(patient_data))
        )


class WranglersTest(AssertResultTestCase):
    MOST_REPEATED = MostRepeatedWrangler()
    AVERAGE = AverageWrangler()

    def test_most_repeated_single(self):
        patient_data = PatientInfo({'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000})
        self._assert_result(
            result=self.MOST_REPEATED([patient_data]),
            expected=patient_data
        )

    def test_most_repeated_many_no_ties(self):
        patients_data = [
            PatientInfo({'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000}),
            PatientInfo({'deductible': 1200, 'stop_loss': 13000, 'oop_max': 6000}),
            PatientInfo({'deductible': 1000, 'stop_loss': 10000, 'oop_max': 6000}),
            PatientInfo({'deductible': 1200, 'stop_loss': 10000, 'oop_max': 6000})
        ]
        self._assert_result(
            result=self.MOST_REPEATED(patients_data),
            expected=PatientInfo({'deductible': None, 'stop_loss': 10000, 'oop_max': 6000})
        )

    def test_most_repeated_many_ties(self):
        patients_data = [
            PatientInfo({'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000}),
            PatientInfo({'deductible': 1200, 'stop_loss': 13000, 'oop_max': 6000}),
            PatientInfo({'deductible': 1000, 'stop_loss': 10000, 'oop_max': 6000}),
            PatientInfo({'deductible': 1200, 'stop_loss': 10000, 'oop_max': 6000})
        ]
        result = self.MOST_REPEATED(patients_data, allow_ties=True)
        self.assertIn(result.deductible, (1000, 1200))
        self.assertEqual(result.stop_loss, 10000)
        self.assertEqual(result.oop_max, 6000)

    def test_average_single(self):
        patient_data = PatientInfo({'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000})
        self._assert_result(
            result=self.AVERAGE([patient_data]),
            expected=patient_data
        )

    def test_average_many(self):
        patients_data = [
            PatientInfo({'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000}),
            PatientInfo({'deductible': 1200, 'stop_loss': 13000, 'oop_max': 6000}),
            PatientInfo({'deductible': 1000, 'stop_loss': 10000, 'oop_max': 6000}),
        ]
        self._assert_result(
            result=self.AVERAGE(patients_data),
            expected=PatientInfo({
                'deductible': round((1000 + 1200 + 1000) / 3),
                'stop_loss': round((10000 + 13000 + 10000) / 3),
                'oop_max': round((5000 + 6000 + 6000) / 3)
            })
        )


class PatientQueriesTest(AssertResultTestCase):
    DUMMY_DATA = {
        1: [
            PatientInfo({'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000}),
            PatientInfo({'deductible': 1200, 'stop_loss': 13000, 'oop_max': 6000}),
            PatientInfo({'deductible': 1000, 'stop_loss': 10000, 'oop_max': 6000}),
            PatientInfo({'deductible': 1200, 'stop_loss': 10000, 'oop_max': 6000})
        ]
    }
    DUMMY_SINGLE_WRANGLER = DummyPatientQuery(wranglers=[MostRepeatedWrangler()], dummy_data=DUMMY_DATA)
    DUMMY_CHAINED_WRANGLERS = DummyPatientQuery(wranglers=[MostRepeatedWrangler(), AverageWrangler()], dummy_data=DUMMY_DATA)
    JSON = JSONFilePatientQuery(EXAMPLE_PATIENT_JSON_FILENAME)

    def test_dummy_single_wrangler_no_ties(self):
        self._assert_result(
            result=self.DUMMY_SINGLE_WRANGLER.get_full_patient_info(1),
            expected=Patient({
                'member_id': 1,
                'info': PatientInfo({
                    'deductible': None,
                    'stop_loss': 10000,
                    'oop_max': 6000
                })
            })
        )

    def test_dummy_single_wrangler_ties(self):
        # pylint: disable=no-member
        result = self.DUMMY_SINGLE_WRANGLER.get_full_patient_info(1, allow_ties=True)
        self.assertEqual(result.member_id, 1)
        self.assertIn(result.info.deductible, (1000, 1200))
        self.assertEqual(result.info.stop_loss, 10000)
        self.assertEqual(result.info.oop_max, 6000)

    def test_dummy_chained_wranglers(self):
        self._assert_result(
            result=self.DUMMY_CHAINED_WRANGLERS.get_full_patient_info(1),
            expected=Patient({
                'member_id': 1,
                'info': PatientInfo({
                    'deductible': round((1000 + 1200 + 1000 + 1200) / 4),
                    'stop_loss': 10000,
                    'oop_max': 6000
                })
            })
        )


if __name__ == '__main__':
    unittest.main()
