from db.database import connect
from model.model import ProductDataset
from utils.index import removeUnnecessaryFieldFromDict


def create_product(product_data: dict) -> dict:
    """Create a new product"""
    session = connect()
    product = ProductDataset(**product_data)
    session.add(product)
    session.commit()
    session.close()
    
    return removeUnnecessaryFieldFromDict(product.__dict__, ["_sa_instance_state"])

def get_all_products(limit: int = 50, page: int = 1) -> list:
    """Get all products from product dataset"""
    session = connect()
    products = session.query(ProductDataset).limit(limit).offset((page - 1) * limit).all()
    session.close()
    results =[]
    
    for product in products:
        product_dict = removeUnnecessaryFieldFromDict(product.__dict__, ["_sa_instance_state"])
        results.append(product_dict)

    return results

def get_product_by_id(product_id: str) -> dict:
    """Get a product by product id"""
    session = connect()
    product = session.query(ProductDataset).filter_by(product_id=product_id).first()
    session.close()
    
    if product is None:
        return {}
    
    return removeUnnecessaryFieldFromDict(product.__dict__, ["_sa_instance_state"])

def update_product(product_id: str, update_data: dict) -> dict:
    """Update an existing product by product id"""
    session = connect()
    product = session.query(ProductDataset).filter_by(product_id=product_id).first()

    if product is None:
        session.close()
        return False

    for key, value in update_data.items():
        setattr(product, key, value)

    session.commit()
    session.close()
    
    return removeUnnecessaryFieldFromDict(product.__dict__, ["_sa_instance_state"])

def delete_product(product_id: str) -> bool:
    """Delete a prodcut"""
    session = connect()
    product = session.query(ProductDataset).filter_by(product_id=product_id).first()

    if product is None:
        session.close()
        return False

    session.delete(product)
    session.commit()
    session.close()
    return True
