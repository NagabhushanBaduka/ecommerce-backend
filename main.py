from fastapi import FastAPI
from routes import products, orders
from database import init_db

app = FastAPI(title="E-commerce API")

app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])

@app.on_event("startup")
async def startup_event():
    await init_db()