from app.core.entities.order import Order
from app.infrastructure.models import OrderModel


class OrderMapper:

    @staticmethod
    def model_to_entity(model: OrderModel):
        if not model:
            return None

        return Order(
            id=model.id,
            patient_id=model.patient_id,
            appointment_id=model.appointment_id,
            total_amount=model.total_amount,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def entity_to_model(entity: Order):
        if not entity:
            return None

        return OrderModel(
            id=entity.id,
            patient_id=entity.patient_id,
            appointment_id=entity.appointment_id,
            total_amount=entity.total_amount,
            status=entity.status
        )