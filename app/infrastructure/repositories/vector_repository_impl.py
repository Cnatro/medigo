from sqlalchemy import text
from typing_extensions import override

from app.core.repositories.vector_repository import VectorRepository
from app.infrastructure.db import db


class VectorRepositoryImpl(VectorRepository):

    @override
    def search_symptoms(self, embedding, top_k=5):
        query = text("""
            SELECT s.id, s.name, s.description,
                   s.embedding <=> CAST(:embedding AS vector) AS distance
            FROM symptoms s
            ORDER BY distance
            LIMIT :top_k
        """)

        result = db.session.execute(query, {
            "embedding": embedding,
            "top_k": top_k
        }).fetchall()

        return [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "distance": r.distance,
                "similarity": 1 - r.distance
            }
            for r in result
        ]
