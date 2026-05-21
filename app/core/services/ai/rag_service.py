from app.core.services.ai.embedding_service import EmbeddingService
from app.core.services.ai.ranking_service import RankingService
from app.infrastructure.repositories.doctor_repository_impl import DoctorRepositoryImpl
from app.infrastructure.repositories.specialtie_repository_impl import SpecialtyRepositoryImpl
from app.infrastructure.repositories.symptom_repository_impl import SymptomRepositoryImpl
from app.infrastructure.repositories.time_slot_repository_impl import TimeSlotRepositoryImpl
from app.infrastructure.repositories.vector_repository_impl import VectorRepositoryImpl
import json


class RagService:

    def __init__(self, embed_service: EmbeddingService, vector_repo: VectorRepositoryImpl,
                 symptom_repo: SymptomRepositoryImpl, doctor_repo: DoctorRepositoryImpl,
                 specialty_repo: SpecialtyRepositoryImpl, ranking_service: RankingService,
                 time_slot_repo: TimeSlotRepositoryImpl):
        self.embed_service = embed_service
        self.vector_repo = vector_repo
        self.symptom_repo = symptom_repo
        self.doctor_repo = doctor_repo
        self.specialty_repo = specialty_repo
        self.time_slot_repo = time_slot_repo
        self.ranking_service = ranking_service

    def handle_query(self, user_input: str):
        embedding = self.embed_service.embed(user_input)


        symptoms = self.vector_repo.search_symptoms(embedding)
        symptom_ids = [s["id"] for s in symptoms]

        specialties_raw = self.symptom_repo.map_to_specialties(symptom_ids)
        ranked_specialties = self.ranking_service.specialty_ranking(specialties=specialties_raw,
                                                                    matched_symptoms=symptoms)
        top_specialty_ids = [
            s[0] for s in ranked_specialties[:2]
        ]

        specialty_names = self.specialty_repo.find_names_by_ids(ids=top_specialty_ids)
        doctors = self.doctor_repo.find_doctors_by_specialty_ids(top_specialty_ids)

        ranked_doctor = self.ranking_service.doctor_ranking(doctors=doctors)

        # gợi ý lịch
        doctor_ids = [d["id"] for d in ranked_doctor]

        slots_by_doctor = self.time_slot_repo.get_slots_by_doctor_ids(
            doctor_ids=doctor_ids,
            limit=3
        )
        suggested_slots = []
        for doctor_id, slots in slots_by_doctor.items():
            for s in slots:
                suggested_slots.append({
                    "doctor_id": doctor_id,
                    "id": s.id,
                    "date": str(s.date),
                    "start_time": str(s.start_time),
                    "end_time": str(s.end_time)
                })
        answer = self.embed_service.sumnary_answer(
            user_input=user_input,
            specialty_names=specialty_names
        )

        try:
            answer_data = json.loads(answer)
        except Exception:
            answer_data = {}

        return {
            "symptoms": symptoms,
            "specialties": [
                {
                    "id": s.id,
                    "name": s.name
                }
                for s in specialty_names
            ],
            "doctors": ranked_doctor,
            "suggested_slots": suggested_slots,
            **answer_data
        }
