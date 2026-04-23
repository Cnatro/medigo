from abc import ABC, abstractmethod
from typing import override

from app.core.services.handle_role.update_registry import register_update_role
from app.infrastructure.repositories.doctor_repository_impl import DoctorRepositoryImpl
from app.infrastructure.repositories.patient_repository_impl import PatientRepositoryImpl
from app.shared.utils.role import Role


class BaseUpdateHandle(ABC):

    @abstractmethod
    def update_user(self, user_id, data): pass

@register_update_role(Role.DOCTOR.name)
class DoctorQueryHandle(BaseUpdateHandle):

    def __init__(self, doctor_repo : DoctorRepositoryImpl):
        self.doctor_repo = doctor_repo

    @override
    def update_user(self, user_id, data):
        return self.doctor_repo.update_doctor_by_user_id(user_id=user_id, data=data)


@register_update_role(Role.PATIENT.name)
class PatientQueryHandle(BaseUpdateHandle):

    def __init__(self, patient_repo:PatientRepositoryImpl):
        self.patient_repo = patient_repo


    @override
    def update_user(self, user_id, data):
        return self.patient_repo.update_patient_by_user_id(user_id= user_id, data=data)