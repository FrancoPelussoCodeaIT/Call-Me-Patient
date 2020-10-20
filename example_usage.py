from call_me_patient.patients import JSONFilePatientQuery, DummyPatientQuery
from call_me_patient.wranglers import AverageWrangler, MostRepeatedWrangler


def main():
    m = JSONFilePatientQuery(filename='call_me_patient/example_data.json', wranglers=[MostRepeatedWrangler(), AverageWrangler()])
    info = m.wrangle(m.get_parsed_info())
    m = DummyPatientQuery()
    m_info = m.get_full_patient_info()
    print(f'JSONFile: {info}\nMocked: {m_info}')


if __name__ == '__main__':
    main()
