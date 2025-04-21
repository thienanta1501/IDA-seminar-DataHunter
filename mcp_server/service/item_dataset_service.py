from db.database import connect
from model.model import ItemDataset
from utils.index import removeUnnecessaryFieldFromDict


def create_item(item_data: dict) -> dict:
    """Create new item"""
    session = connect()
    item = ItemDataset(**item_data)
    session.add(item)
    session.commit()
    session.close()
    
    return removeUnnecessaryFieldFromDict(item.__dict__, ["_sa_instance_state"])

def get_all_items(limit: int = 50, page: int = 1) -> list:
    """Get all items from item dataset"""
    session = connect()
    items = session.query(ItemDataset).limit(limit).offset((page - 1) * limit).all()
    session.close()
    results = []
    
    for item in items:
        item_dict = removeUnnecessaryFieldFromDict(item.__dict__, ["_sa_instance_state"])
        results.append(item_dict)
        
    return results

def get_item_by_id(order_id: str, order_item_id: int) -> dict:
    """Get item by order item id and order id"""
    session = connect()
    item = session.query(ItemDataset).filter_by(order_id=order_id, order_item_id=order_item_id).first()
    session.close()
    
    if item is None:
        return {}
    
    return removeUnnecessaryFieldFromDict(item.__dict__, ["_sa_instance_state"])

def update_item(order_id: str, order_item_id: int, updated_data: dict) -> dict:
    """Update an existing item"""
    session = connect()
    item = session.query(ItemDataset).filter_by(order_id=order_id, order_item_id=order_item_id).first()
    
    if item is None:
        session.close()
        return {}
    
    for key, value in updated_data.items():
        setattr(item, key, value)
        
    session.commit()
    session.close()
    
    return removeUnnecessaryFieldFromDict(item.__dict__, ["_sa_instance_state"])

def delete_item(order_id: str, order_item_id: int) -> bool:
    """Delete an item"""
    session = connect()
    item = session.query(ItemDataset).filter_by(order_id=order_id, order_item_id=order_item_id).first()
    
    if item is None:
        session.close()
        return False
    
    session.delete(item)
    session.commit()
    session.close()
    return True

