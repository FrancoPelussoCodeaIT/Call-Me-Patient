from call_me_patient.patients import JSONFilePatientQuery, DummyPatientQuery
from call_me_patient.wranglers import AverageWrangler, MostRepeatedWrangler


def main():
    m = JSONFilePatientQuery(
        filename='call_me_patient/example_data.json',
        # You may specify multiple wranglers to be used, they will be called sequentally to fill in any empty fields.
        wranglers=[MostRepeatedWrangler(), AverageWrangler()]
    )
    info = m.get_full_patient_info(1)
    m = DummyPatientQuery()
    m_info = m.get_full_patient_info()  # You may leave the member_id empty if the Wrangler and Query support it.
    print(
        f'JSONFilePatientQuery: {info}\n'
        f'DummyPatientQuery: {m_info}'
    )


if __name__ == '__main__':
    main()
