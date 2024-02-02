from fastapi import FastAPI, Query,HTTPException,Body,Request
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from typing import Optional
from bson import ObjectId
from datetime import datetime, timezone,timedelta

app = FastAPI()

from mongo_queries import get_products_collection, insert_dummy_products, query_products, get_orders_collection, insert_order

products_collection = get_products_collection()
orders_collection = get_orders_collection()

insert_dummy_products(products_collection)


@app.get("/products/")
async def list_products(
    limit: int = Query(10, description="Number of records to return", ge=1, le=100),
    offset: int = Query(0, description="Offset from where to start", ge=0),
    min_price: Optional[float] = Query(None, description="Minimum product price"),
    max_price: Optional[float] = Query(None, description="Maximum product price"),
):
   
    query = {}
    if min_price is not None:
        query["price"] = {"$gte": min_price}
    if max_price is not None:
        query["price"] = {**query.get("price", {}), "$lte": max_price}

    
    records = (
        products_collection.find(query)
        .limit(limit)
        .skip(offset)
    )

   
    total = products_collection.count_documents(query)

 
    next_offset = offset + limit if offset + limit < total else None
    prev_offset = offset - limit if offset - limit >= 0 else None

   
    data = [
        {"id": str(record["_id"]), "name": record["name"], "price": record["price"], "quantity": record["quantity"]}
        for record in records
    ]
    response_data = {
        "data": data,
        "page": {"limit": limit, "nextOffset": next_offset, "prevOffset": prev_offset, "total": total},
    }

    return JSONResponse(content=response_data)

@app.post("/orders/")
async def create_order(request: Request):
    order_data = await request.json()

    items = order_data.get("items", [])
    user_address = order_data.get("user_address", {})

   
    for item in items:
        if not all(key in item for key in ("productId", "boughtQuantity", "totalAmount")):
            raise HTTPException(status_code=400, detail="Invalid items format")

   
    total_amount = sum(item["totalAmount"] for item in items)

 
    order_data = {
        "createdOn": datetime.now(timezone(timedelta(hours=5, minutes=30))).isoformat(),  # Will be auto-generated
        "items": items,
        "totalAmount": total_amount,
        "userAddress": user_address,
    }

   
    order_id = insert_order(order_data)

 
    inserted_order = orders_collection.find_one({"_id": ObjectId(order_id)})

   
    response_data = {
        "id": str(inserted_order["_id"]),
        "createdOn": inserted_order["createdOn"],
        "items": inserted_order["items"],
        "totalAmount": inserted_order["totalAmount"],
        "userAddress": inserted_order["userAddress"],
    }

    return JSONResponse(content=response_data)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
