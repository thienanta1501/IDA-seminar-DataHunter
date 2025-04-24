from sqlalchemy import Column, String, Integer, Float, DateTime
from db.database import Base

class OrderDataset(Base):
    __tablename__ = 'order_dataset'
    order_id = Column(String(32), primary_key=True)
    customer_id = Column(String(32), primary_key=True)
    order_status = Column(String, nullable=False)
    order_purchase_timestamp = Column(DateTime, nullable=False)
    order_delivered_customer_date = Column(DateTime)

class ReviewDataset(Base):
    __tablename__ = 'review_dataset'
    review_id = Column(String(32), primary_key=True)
    order_id = Column(String(32), primary_key=True)
    review_score = Column(Integer)

class CustomerDataset(Base):
    __tablename__ = "customer_dataset"
    customer_id = Column(String(32), primary_key=True)
    customer_unique_id = Column(String(32), primary_key=True)
    customer_city = Column(String)

class ItemDataset(Base):
    __tablename__ = "item_dataset"
    order_id = Column(String(32), primary_key=True)
    order_item_id = Column(Integer, primary_key=True)
    product_id = Column(String(32))
    price = Column(Float)
    freight_value = Column(Float)

class PaymentDataset(Base):
    __tablename__ = "payment_dataset"
    order_id = Column(String(32), primary_key=True)
    payment_sequential = Column(Integer, primary_key=True)
    payment_type = Column(String)
    payment_installments = Column(Integer)
    payment_value = Column(Float)

class ProductDataset(Base):
    __tablename__ = "product_dataset"
    product_id = Column(String(32), primary_key=True)
    product_category_name = Column(String)
    product_weight_g = Column(Float)
    product_length_cm = Column(Float)
    product_height_cm = Column(Float)
    product_width_cm = Column(Float)
