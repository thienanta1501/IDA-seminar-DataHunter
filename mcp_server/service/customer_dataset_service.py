from db.database import connect
from model.model import CustomerDataset
from utils.index import removeUnnecessaryFieldFromDict


def create_customer(customer_data: dict) -> dict:
    """Create new customer"""
    session = connect()
    customer = CustomerDataset(**customer_data)
    session.add(customer)
    session.commit()
    session.close()
    
    return removeUnnecessaryFieldFromDict(customer.__dict__, ["_sa_instance_state"])
    
def get_all_customers(limit: int = 50, page: int = 1) -> list:
    """Get all customers from customer dataset"""
    session = connect()
    customers = session.query(CustomerDataset).limit(limit).offset((page - 1) * limit).all()
    session.close()
    results = []
    
    for customer in customers:
        customer_dict = removeUnnecessaryFieldFromDict(customer.__dict__, ["_sa_instance_state"])
        results.append(customer_dict)

    return results

def get_customer_by_id(customer_id: str, customer_unique_id: str) -> dict:
    """Get a customer by customer_id and customer_unique_id"""
    session = connect()
    customer = session.query(CustomerDataset).filter_by(customer_id=customer_id, customer_unique_id=customer_unique_id).first()
    session.close()

    if customer is None:
        return {}

    return removeUnnecessaryFieldFromDict(customer.__dict__, ["_sa_instance_state"])

def update_customer(customer_id: str, customer_unique_id: str, updated_data: dict) -> dict:
    """Update existing customer"""
    session = connect()
    customer = session.query(CustomerDataset).filter_by(customer_id=customer_id, customer_unique_id=customer_unique_id).first()

    if customer is None:
        session.close()
        return {}

    for key, value in updated_data.items():
        setattr(customer, key, value)

    session.commit()
    session.close()
    
    return removeUnnecessaryFieldFromDict(customer.__dict__, ["_sa_instance_state"])

def delete_customer(customer_id: str, customer_unique_id: str) -> bool:
    """Delete customer by ID"""
    session = connect()
    customer = session.query(CustomerDataset).filter_by(customer_id=customer_id, customer_unique_id=customer_unique_id).first()

    if customer is None:
        session.close()
        return False

    session.delete(customer)
    session.commit()
    session.close()
    return True
