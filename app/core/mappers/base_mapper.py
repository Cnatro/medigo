def to_entity(model, entity_class):
    data = {
        k: v for k, v in model.__dict__.items()
        if not k.startswith("_")
        and not isinstance(v, (list, dict))  # tránh relationship
    }
    return entity_class(**data)


def to_model(entity, model_class):
    return model_class(**entity.__dict__)