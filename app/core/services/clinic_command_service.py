from app.infrastructure.repositories.clinic_repository_impl import ClinicRepositoryImpl


class ClinicCommandService:
    def __init__(self, clinic_repo: ClinicRepositoryImpl):
        self.clinic_repo = clinic_repo
