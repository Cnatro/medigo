from app.infrastructure.repositories.doctor_repository_impl import DoctorRepositoryImpl


class DoctorCommandService:
    def __init__(self, doctor_repo : DoctorRepositoryImpl):
        self.doctor_repo = doctor_repo