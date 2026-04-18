from abc import ABC, abstractmethod
from typing import override

from app.core.entities.doctor import Doctor
from app.core.entities.patient import Patient
from app.core.services.handle_role.registry import register_role
from app.shared.utils.role import Role


class BaseHandle(ABC):

    @abstractmethod
    def handle(self, user, profile):
        pass


@register_role(Role.DOCTOR.name)
class DoctorRoleHandler(BaseHandle):

    def __init__(self, doctor_repo):
        self.doctor_repo = doctor_repo

    @override
    def handle(self, user, profile):
        doctor = Doctor(
            id=None,
            user_id=user.id,
            bio=profile.get("bio"),
            experience_years=profile.get("experience_years"),
            clinic_id=profile.get("clinic_id"),
            rating_avg=0,
            total_reviews=0
        )

        self.doctor_repo.save(doctor)


@register_role(Role.PATIENT.name)
class PatientRoleHandler(BaseHandle):

    def __init__(self, patient_repo):
        self.patient_repo = patient_repo

    @override
    def handle(self, user, profile):
        patient = Patient(
            id=None,
            user_id=user.id,
            date_of_birth=profile.get("date_of_birth"),
            gender=profile.get("gender")
        )

        self.patient_repo.save(patient)
