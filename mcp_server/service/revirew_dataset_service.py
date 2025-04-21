from db.database import connect
from model.model import ReviewDataset
from utils.index import removeUnnecessaryFieldFromDict


def create_review(new_review: dict) -> dict:
    """Create a new review"""
    session = connect()
    review = ReviewDataset(**new_review)
    session.add(review)
    session.commit()
    session.close()
    
    return removeUnnecessaryFieldFromDict(new_review.__dict__, ["_sa_instance_state"])

def get_all_reviews(limit: int = 50, page: int = 1) -> list:
    """Get all reviews from review dataset"""
    session = connect()
    reviews = session.query(ReviewDataset).limit(limit).offset((page - 1) * limit).all()
    session.close()
    results = []
    
    for review in reviews:
        review_dict = removeUnnecessaryFieldFromDict(review.__dict__, ["_sa_instance_state"])
        results.append(review_dict)
        
    return results

def get_review_by_id(review_id: str, order_id: str) -> dict:
    """Get a review by its review id and order id"""
    session = connect()
    review = session.query(ReviewDataset).filter_by(review_id=review_id, order_id=order_id).first()
    session.close()
    
    if review is None:
        return {}
    
    return removeUnnecessaryFieldFromDict(review.__dict__, ["_sa_instance_state"])

def update_review(review_id: str, order_id: str, update_data: dict) -> dict:
    """Update an existing review by its review id and order id"""
    session = connect()
    review = session.query(ReviewDataset).filter_by(review_id=review_id, order_id=order_id).first()
    
    if review is None:
        session.close()
        return {}

    for key, value in update_data.items():
        setattr(review, key, value)

    session.commit()
    session.close()
    
    return removeUnnecessaryFieldFromDict(review.__dict__, ["_sa_instance_state"])

def delete_review(review_id: str, order_id: str) -> bool:
    """Delete a review """
    session = connect()
    review = session.query(ReviewDataset).filter_by(review_id=review_id, order_id=order_id).first()
    
    if review is None:
        session.close()
        return False

    session.delete(review)
    session.commit()
    session.close()
    return True
