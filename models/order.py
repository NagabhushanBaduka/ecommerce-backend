from pydantic import BaseModel
from typing import List
from models.product import Pagination

class OrderItem(BaseModel):
    productId: str
    qty: int

class OrderCreate(BaseModel):
    userId: str
    items: List[OrderItem]

class ProductDetails(BaseModel):
    id: str
    name: str

class OrderItemOut(BaseModel):
    productDetails: ProductDetails
    qty: int

class OrderOut(BaseModel):
    id: str
    items: List[OrderItemOut]
    total: float

class OrderListResponse(BaseModel):
    data: List[OrderOut]
    page: Pagination