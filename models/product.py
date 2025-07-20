from pydantic import BaseModel
from typing import  List

class SizeModel(BaseModel):
    size: str
    quantity: int

class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: List[SizeModel]

class ProductOut(BaseModel):
    id: str

class ProductListItem(BaseModel):
    id: str
    name: str
    price: float

class Pagination(BaseModel):
    next: int
    limit: int
    previous: int

class ProductListResponse(BaseModel):
    data: List[ProductListItem]
    page: Pagination