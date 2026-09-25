from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import uuid
from pathlib import Path
from backend.database import get_connection
from backend.config import BASE_DIR

router = APIRouter(prefix="/api/products", tags=["digital_products"])

class PurchaseRequest(BaseModel):
    product_slug: str
    customer_email: str
    payment_provider: str = "stripe"

@router.get("/list")
def list_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM digital_products ORDER BY price_usd DESC")
    rows = cursor.fetchall()
    conn.close()
    
    products = []
    for r in rows:
        p = dict(r)
        if p.get("features_json"):
            p["features"] = json.loads(p["features_json"])
        products.append(p)
        
    return {"status": "success", "products": products}

@router.post("/purchase")
def simulate_or_record_purchase(payload: PurchaseRequest):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM digital_products WHERE slug = ?", (payload.product_slug,))
    prod = cursor.fetchone()
    if not prod:
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")
        
    # Create transaction record
    tx_id = f"tx_{uuid.uuid4().hex[:16]}"
    cursor.execute("""
        INSERT INTO transactions (id, user_id, customer_email, product_id, amount, currency, provider, status)
        VALUES (?, NULL, ?, ?, ?, 'USD', ?, 'completed')
    """, (tx_id, payload.customer_email, prod["id"], prod["price_usd"], payload.payment_provider))
    
    # Increment sales count
    cursor.execute("""
        UPDATE digital_products SET sales_count = sales_count + 1 WHERE id = ?
    """, (prod["id"],))
    
    conn.commit()
    conn.close()
    
    download_link = f"/api/products/download/{payload.product_slug}?token={tx_id}"
    
    return {
        "status": "success",
        "message": f"Successfully purchased {prod['title']}!",
        "transaction_id": tx_id,
        "amount": prod["price_usd"],
        "download_url": download_link
    }

@router.get("/download/{slug}")
def download_digital_product(slug: str, token: str = ""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM digital_products WHERE slug = ?", (slug,))
    prod = cursor.fetchone()
    conn.close()
    
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
        
    file_path = BASE_DIR / prod["file_path"]
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Product file not found on disk")
        
    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type="application/octet-stream"
    )
