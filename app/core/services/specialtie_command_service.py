from app.infrastructure.repositories.specialtie_repository_impl import SpecialtyRepositoryImpl


class SpecialtyCommandService:
    def __init__(self, specialty_repo : SpecialtyRepositoryImpl):
        self.specialty_repo = specialty_repo