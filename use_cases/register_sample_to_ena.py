from domain.entities.sample_registration import SampleRegistration
from schemas.sample_accessions import SampleAccessions


def register_sample_to_ena(sample_registration: SampleRegistration) -> SampleAccessions:
    return sample_registration.register_sample()
