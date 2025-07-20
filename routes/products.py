from fastapi import APIRouter, Query
from models.product import ProductCreate, ProductOut, ProductListItem, ProductListResponse, Pagination
from database import db
from bson import ObjectId
from typing import List, Optional

router = APIRouter()

@router.post("/", status_code=201, response_model=ProductOut)
async def create_product(product: ProductCreate):
    result = await db.products.insert_one(product.dict())
    return {"id": str(result.inserted_id)}

@router.get("/", response_model=ProductListResponse)
async def list_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["sizes.size"] = size

    cursor = db.products.find(query).skip(offset).limit(limit)
    data = []
    async for doc in cursor:
        data.append({
            "id": str(doc["_id"]),
            "name": doc["name"],
            "price": doc["price"]
        })

    page_info = {
        "next": offset + limit,
        "limit": len(data),
        "previous": offset - limit
    }
    return {"data": data, "page": page_info}