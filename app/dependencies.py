import cloudinary

from app.config import Config
from app.core.services.ai import ranking_service
from app.core.services.ai.embedding_service import EmbeddingService
from app.core.services.ai.rag_service import RagService
from app.core.services.ai.ranking_service import RankingService
from app.core.services.appointment_command_service import AppointmentCommandService
from app.core.services.clinic_command_service import ClinicCommandService
from app.core.services.clinic_query_service import ClinicQueryService
from app.core.services.doctor_command_service import DoctorCommandService
from app.core.services.doctor_query_service import DoctorQueryService
from app.core.services.handle_role.query_registry import ROLE_QUERY_HANDLERS
from app.core.services.handle_role.registry import ROLE_HANDLES
from app.core.services.handle_role.update_registry import ROLE_UPDATE_HANDLERS
from app.core.services.order_command_service import OrderCommandService
from app.core.services.order_query_service import OrderQueryService
from app.core.services.payment.momo_service import MomoService
from app.core.services.schedule_command_service import ScheduleCommandService
from app.core.services.schedule_query_service import ScheduleQueryService
from app.core.services.specialtie_query_service import SpecialtyQueryService
from app.core.services.time_slot_command_service import TimeSlotCommandService
from app.core.services.time_slot_query_service import TimeSlotQueryService
from app.core.services.user_command_service import UserCommandService
from app.core.services.user_query_service import UserQueryService
from app.infrastructure.repositories.appointment_repository_impl import AppointmentRepositoryImpl
from app.infrastructure.repositories.clinic_repository_impl import ClinicRepositoryImpl
from app.infrastructure.repositories.doctor_repository_impl import DoctorRepositoryImpl
from app.infrastructure.repositories.order_repository_impl import OrderRepositoryImpl
from app.infrastructure.repositories.patient_repository_impl import PatientRepositoryImpl
from app.infrastructure.repositories.payment_history_repository_impl import PaymentHistoryRepositoryImpl
from app.infrastructure.repositories.schedule_repository_impl import ScheduleRepositoryImpl
from app.infrastructure.repositories.specialtie_repository_impl import SpecialtyRepositoryImpl
from app.infrastructure.repositories.symptom_repository_impl import SymptomRepositoryImpl
from app.infrastructure.repositories.time_slot_repository_impl import TimeSlotRepositoryImpl
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.vector_repository_impl import VectorRepositoryImpl
from app.shared.utils.role import Role

import app.core.services.handle_role


def get_user_repo():
    return UserRepositoryImpl()


def get_role_command_handlers():
    return {
        Role.DOCTOR.name: ROLE_HANDLES[Role.DOCTOR.name](DoctorRepositoryImpl()),
        Role.PATIENT.name: ROLE_HANDLES[Role.PATIENT.name](PatientRepositoryImpl()),
    }


def get_role_query_handlers():
    return {
        Role.DOCTOR.name: ROLE_QUERY_HANDLERS[Role.DOCTOR.name](DoctorRepositoryImpl()),
        Role.PATIENT.name: ROLE_QUERY_HANDLERS[Role.PATIENT.name](PatientRepositoryImpl())
    }


def get_role_update_handlers():
    return {
        Role.DOCTOR.name: ROLE_UPDATE_HANDLERS[Role.DOCTOR.name](DoctorRepositoryImpl()),
        Role.PATIENT.name: ROLE_UPDATE_HANDLERS[Role.PATIENT.name](PatientRepositoryImpl()),
    }


def get_user_command_service():
    repo = get_user_repo()
    role_handlers = get_role_command_handlers()

    return UserCommandService(
        repo=repo,
        role_handlers=role_handlers,
        role_update_handlers=get_role_update_handlers()
    )


def get_user_query_service():
    repo = get_user_repo()
    role_query_handlers = get_role_query_handlers()
    return UserQueryService(
        repo=repo,
        role_query_handlers=role_query_handlers
    )


def get_order_repo():
    return OrderRepositoryImpl()


def get_order_command_service():
    payment_history_repo = PaymentHistoryRepositoryImpl()
    momo_service = MomoService(payment_repo=payment_history_repo)
    return OrderCommandService(
        order_repo=get_order_repo(),
        momo_service=momo_service
    )


def get_order_query_service():
    return OrderQueryService(
        order_repo=get_order_repo()
    )


def get_doctor_query_service():
    return DoctorQueryService(
        doctor_repo=DoctorRepositoryImpl()
    )


def get_doctor_command_service():
    return DoctorCommandService(
        doctor_repo=DoctorRepositoryImpl()
    )


def get_clinic_query_service():
    return ClinicQueryService(
        clinic_repo=ClinicRepositoryImpl()
    )


def get_clinic_command_service():
    return ClinicCommandService(
        clinic_repo=ClinicRepositoryImpl()
    )


def get_specialty_query_service():
    return SpecialtyQueryService(
        specialty_repo=SpecialtyRepositoryImpl()
    )


def get_specialty_command_service():
    return SpecialtyQueryService(
        specialty_repo=SpecialtyRepositoryImpl()
    )


def get_time_slot_query_service():
    return TimeSlotQueryService(
        time_slot_repo=TimeSlotRepositoryImpl()
    )


def init_cloudinary():
    cloudinary.config(
        cloud_name=Config.CLOUDINARY_CLOUD_NAME,
        api_key=Config.CLOUDINARY_API_KEY,
        api_secret=Config.CLOUDINARY_API_SECRET
    )


def get_rag_service():
    return RagService(
        embed_service=EmbeddingService(),
        vector_repo=VectorRepositoryImpl(),
        doctor_repo=DoctorRepositoryImpl(),
        symptom_repo=SymptomRepositoryImpl(),
        specialty_repo=SpecialtyRepositoryImpl(),
        ranking_service=RankingService()
    )

def get_appointment_command_service():
    return AppointmentCommandService(
        appointment_repo= AppointmentRepositoryImpl(),
        time_slot_repo= TimeSlotRepositoryImpl(),
    )

def get_time_slot_command_service():
    return TimeSlotCommandService(
        time_slot_repo=TimeSlotRepositoryImpl()
    )


def get_schedule_command_service():
    return ScheduleCommandService(
        doctor_repo=DoctorRepositoryImpl(),
        schedule_repo=ScheduleRepositoryImpl(),
        timeslot_command_service=get_time_slot_command_service()
    )


def get_schedule_query_service():
    return ScheduleQueryService(
        schedule_repo=ScheduleRepositoryImpl(),
        user_repo=UserRepositoryImpl(),
        time_slot_repo=TimeSlotRepositoryImpl()
    )
