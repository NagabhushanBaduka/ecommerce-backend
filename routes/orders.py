from fastapi import APIRouter
from models.order import OrderCreate, OrderListResponse
from database import db
from datetime import datetime
from bson import ObjectId
from typing import List

router = APIRouter()

@router.post("/", status_code=201)
async def create_order(order: OrderCreate):
    order_dict = {
        "user_id": order.userId,
        "items": [item.dict() for item in order.items],
        "created_at": datetime.utcnow()
    }
    result = await db.orders.insert_one(order_dict)
    return {"id": str(result.inserted_id)}

@router.get("/{user_id}", response_model=OrderListResponse)
async def get_orders(user_id: str, limit: int = 10, offset: int = 0):
    cursor = db.orders.find({"user_id": user_id}).skip(offset).limit(limit)
    data = []
    async for order in cursor:
        items_out = []
        total = 0.0
        for item in order.get("items", []):
            product = await db.products.find_one({"_id": ObjectId(item["productId"])})
            if product:
                item_total = product["price"] * item["qty"]
                total += item_total
                items_out.append({
                    "productDetails": {
                        "id": str(product["_id"]),
                        "name": product["name"]
                    },
                    "qty": item["qty"]
                })
        data.append({
            "id": str(order["_id"]),
            "items": items_out,
            "total": total
        })
    page_info = {
        "next": offset + limit,
        "limit": len(data),
        "previous": offset - limit
    }
    return {"data": data, "page": page_info}