from db.database import connect
from model.model import OrderDataset
from utils.index import removeUnnecessaryFieldFromDict


def create_order(order_data: dict) -> dict:
    """Create a new order"""
    session = connect()
    order = OrderDataset(**order_data)
    session.add(order)
    session.commit()
    session.close()

    return removeUnnecessaryFieldFromDict(order.__dict__, ["_sa_instance_state"])

def get_all_orders(limit: int = 50, page: int = 1) -> list:
    """Get all orders from order dataset"""
    session = connect()
    orders = session.query(OrderDataset).limit(limit).offset((page - 1) * limit).all()
    session.close()
    results = []

    for order in orders:
        order_dict = removeUnnecessaryFieldFromDict(order.__dict__, ["_sa_instance_state"])
        results.append(order_dict)

    return results

def get_order_by_id(order_id: str, customer_id: str) -> dict:
    """Get order by order id and customer id"""
    session = connect()

    order = session.query(OrderDataset).filter(
        order_id=order_id,
        customer_id=customer_id
    ).first()

    session.close()

    if order is None:
        return {}

    order_dict = removeUnnecessaryFieldFromDict(order.__dict__, ["_sa_instance_state"])
    return order_dict

def update_order(order_id: str, customer_id: str, updated_data: dict) -> dict:
    """Update an existing order"""
    session = connect()
    order = session.query(OrderDataset).filter(
        order_id == order_id,
        customer_id == customer_id
    ).first()
    
    if order is None:
        session.close()
        return {}

    for key, value in updated_data.items():
        setattr(order, key, value)

    session.commit()
    session.close()
    return removeUnnecessaryFieldFromDict(order.__dict__, ["_sa_instance_state"])

def delete_order(order_id: str, customer_id:str) -> bool:
    """Delete an order"""
    session = connect()
    order = session.query(OrderDataset).filter_by(order_id=order_id, customer_id=customer_id).first()
    
    if order is None:
        session.close()
        return False

    session.delete(order)
    session.commit()
    session.close()
    return True
