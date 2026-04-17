from abc import ABC, abstractmethod
from typing import override

from app.core.services.handle_role.query_registry import register_query_role
from app.shared.utils.role import Role


class BaseQueryHandle(ABC):

    @abstractmethod
    def get_profile(self, user_id): pass

@register_query_role(Role.DOCTOR.name)
class DoctorQueryHandle(BaseQueryHandle):

    def __init__(self, doctor_repo):
        self.doctor_repo = doctor_repo

    @override
    def get_profile(self, user_id):
        return self.doctor_repo.find_by_user_id(user_id=user_id)

@register_query_role(Role.PATIENT.name)
class PatientQueryHandle(BaseQueryHandle):

    def __init__(self, patient_repo):
        self.patient_repo = patient_repo


    @override
    def get_profile(self, user_id):
        return self.patient_repo.find_by_user_id(user_id= user_id)
