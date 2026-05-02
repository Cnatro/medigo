from sqlalchemy import text
from typing_extensions import override

from app.core.repositories.symptom_repository import SymptomRepository
from app.infrastructure.db import db


class SymptomRepositoryImpl(SymptomRepository):

    @override
    def map_to_specialties(self, symptom_ids):
        query = text("""
                    SELECT 
                        ss.specialty_id,
                        ss.symptom_id,
                        ss.weight
                    FROM symptom_specialties ss
                    WHERE ss.symptom_id = ANY(:symptom_ids)
                """)

        result = db.session.execute(query, {
            "symptom_ids": symptom_ids
        }).fetchall()

        return result
