from domain.entities.sample_registration import SampleRegistration
from use_cases.register_sample_to_ena import register_sample_to_ena

if __name__ == "__main__":
    sample_set_xml_path = '/Users/oliverkubicka/Desktop/cuspuk/pv_data/sequence_submit/283/test/uvzsr-PT_24_00014-A12-AR_24_00000940 2/sample.xml'
    submission_xml_path = '/Users/oliverkubicka/Desktop/cuspuk/pv_data/sequence_submit/283/test/uvzsr-PT_24_00014-A12-AR_24_00000940 2/submission.xml'

    sample_registration = SampleRegistration(
        sample_set_xml_path=sample_set_xml_path,
        submission_xml_path=submission_xml_path,
        ena_username='Webin-42704',
        ena_password='Kubicka2021',
        results_dir='./',
        test=True
    )
    register_sample_to_ena(sample_registration=sample_registration)

