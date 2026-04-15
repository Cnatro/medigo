from app.core.entities.base_entity import BaseEntity


class Doctor(BaseEntity):
    def __init__(self, id, user_id, bio, experience_years, clinic_id,
                 rating_avg=0, total_reviews=0, embedding=None, created_at=None):
        super().__init__(id)
        self.user_id = user_id
        self.bio = bio
        self.experience_years = experience_years
        self.clinic_id = clinic_id
        self.rating_avg = rating_avg
        self.total_reviews = total_reviews
        self.embedding = embedding
        self.created_at = created_at