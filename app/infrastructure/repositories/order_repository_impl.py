from sqlalchemy.exc import SQLAlchemyError
from typing_extensions import override

from app.core.entities.order import Order
from app.core.repositories.order_repository import OrderRepository
from app.infrastructure.db import db
from app.infrastructure.models import OrderModel
from app.interfaces.mappers.order_mapper import OrderMapper
from app.shared.utils.payment_enum import OrderStatus


class OrderRepositoryImpl(OrderRepository):

    @override
    def save(self, order : Order):
        model = OrderMapper.entity_to_model(order)

        db.session.add(model)
        db.session.commit()
        db.session.refresh(model)

        return OrderMapper.model_to_entity(model)

    @override
    def find_by_id(self, id ):
        model = OrderModel.query.filter_by(id=id).first()

        return OrderMapper.model_to_entity(model)

    @override
    def update_order_status(self, order_id, status : OrderStatus):
        model = OrderModel.query.filter_by(id=order_id).first()

        if not model:
            raise ValueError("Order not found")

        if model.status == status.name:
            return OrderMapper.model_to_entity(model)

        try:
            model.status = status.name
            db.session.commit()
            return OrderMapper.model_to_entity(model)

        except SQLAlchemyError:
            db.session.rollback()
            raise