from domain.entities.assembly_submission import AssemblySubmission


def submit_assembly_to_ena(assembly_submission: AssemblySubmission):
    assembly_submission.submit_assembly()

