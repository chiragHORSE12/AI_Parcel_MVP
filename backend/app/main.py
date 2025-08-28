from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import os
from . import scan
app = FastAPI(title="AI Parcel MVP - Backend")

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(os.path.abspath(UPLOAD_DIR), exist_ok=True)

class OrderCreate(BaseModel):
    customer_name: str
    pickup_address: str
    dropoff_address: str
    weight_kg: float = 0.0

orders = []
order_id_seq = 1

@app.post("/orders", response_model=dict)
def create_order(payload: OrderCreate):
    global order_id_seq
    order = payload.dict()
    order["id"] = order_id_seq
    order["status"] = "created"
    orders.append(order)
    order_id_seq += 1
    return {"success": True, "order": order}

@app.get("/orders", response_model=dict)
def list_orders():
    return {"count": len(orders), "orders": orders}

@app.post("/scan")
async def scan_image(file: UploadFile = File(...)):
    # save upload
    data = await file.read()
    fname = file.filename or "upload.jpg"
    safe_name = fname.replace(" ", "_")
    path = os.path.join(os.path.abspath(UPLOAD_DIR), safe_name)
    with open(path, "wb") as f:
        f.write(data)
    try:
        result = scan.decode_image(path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return JSONResponse({"filename": safe_name, "result": result})
