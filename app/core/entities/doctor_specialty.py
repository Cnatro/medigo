from app.core.entities.base_entity import BaseEntity


class DoctorSpecialty(BaseEntity):
    def __init__(self,id, doctor_id, specialty_id, consultation_fee):

        super().__init__(id)
        self.doctor_id = doctor_id
        self.specialty_id = specialty_id
        self.consultation_fee = consultation_fee