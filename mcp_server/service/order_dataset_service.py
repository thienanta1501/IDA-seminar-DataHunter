from db.database import connect
from model.model import OrderDataset
from utils.index import removeUnnecessaryFieldFromDict


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