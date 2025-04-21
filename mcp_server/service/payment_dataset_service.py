from db.database import connect
from model.model import PaymentDataset
from utils.index import removeUnnecessaryFieldFromDict


def create_payment(payment_data: dict) -> dict:
    """Create a new payment record"""
    session = connect()
    payment = PaymentDataset(**payment_data)
    session.add(payment)
    session.commit()
    session.close()
    
    return removeUnnecessaryFieldFromDict(payment.__dict__, ["_sa_instance_state"])
     
def get_all_payments(limit: int = 50, page: int = 1) -> list:
    """Get all payment records"""
    session = connect()
    payments = session.query(PaymentDataset).limit(limit).offset((page - 1) * limit).all()
    session.close()
    results = []
    
    for payment in payments:
        payment_dict = removeUnnecessaryFieldFromDict(payment.__dict__, ["_sa_instance_state"])
        results.append(payment_dict)

    return results

def get_payment_by_id(order_id: str, payment_sequential: int) -> dict:
    """Get a specific payment record by order_id and payment_sequential"""
    session = connect()
    payment = session.query(PaymentDataset).filter_by(order_id=order_id,payment_sequential=payment_sequential).first()
    session.close()

    if payment is None:
        return {}

    return removeUnnecessaryFieldFromDict(payment.__dict__, ["_sa_instance_state"])

def update_payment(order_id: str, payment_sequential: int, updated_data: dict) -> dict:
    """Update an existing payment record"""
    session = connect()
    payment = session.query(PaymentDataset).filter_by(order_id=order_id, payment_sequential=payment_sequential).first()

    if payment is None:
        session.close()
        return {}

    for key, value in updated_data.items():
        setattr(payment, key, value)

    session.commit()
    session.close()
    
    return removeUnnecessaryFieldFromDict(payment.__dict__, ["_sa_instance_state"])

def delete_payment(order_id: str, payment_sequential: int) -> bool:
    """Delete a payment record"""
    session = connect()
    payment = session.query(PaymentDataset).filter_by(order_id=order_id, payment_sequential=payment_sequential).first()

    if payment is None:
        session.close()
        return False

    session.delete(payment)
    session.commit()
    session.close()
    return True
