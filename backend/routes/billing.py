from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
from backend.database import get_connection
from backend.config import PRICING_PLANS

router = APIRouter(prefix="/api/billing", tags=["billing"])

class UpgradePlanRequest(BaseModel):
    user_email: str
    plan: str # starter, pro, agency
    billing_cycle: str = "monthly" # monthly, yearly
    payment_method: str = "stripe"

class AddCreditsRequest(BaseModel):
    user_email: str
    amount_credits: int
    cost_usd: float

@router.get("/plans")
def get_plans():
    return {"status": "success", "plans": PRICING_PLANS}

@router.post("/subscribe")
def subscribe_plan(payload: UpgradePlanRequest):
    if payload.plan not in PRICING_PLANS:
        raise HTTPException(status_code=400, detail="Invalid plan selected")
        
    plan_info = PRICING_PLANS[payload.plan]
    amount = plan_info["price_monthly"] if payload.billing_cycle == "monthly" else plan_info["price_yearly"]
    credits_to_add = plan_info["credits"]
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE email = ?", (payload.user_email,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
        
    # Record transaction
    tx_id = f"sub_{uuid.uuid4().hex[:16]}"
    cursor.execute("""
        INSERT INTO transactions (id, user_id, customer_email, product_id, amount, currency, provider, status)
        VALUES (?, ?, ?, ?, ?, 'USD', ?, 'completed')
    """, (tx_id, user["id"], user["email"], f"plan_{payload.plan}", amount, payload.payment_method))
    
    # Update user plan and add monthly credits
    cursor.execute("""
        UPDATE users SET plan = ?, credits = credits + ? WHERE id = ?
    """, (payload.plan, credits_to_add, user["id"]))
    
    conn.commit()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user["id"],))
    updated_user = cursor.fetchone()
    conn.close()
    
    return {
        "status": "success",
        "message": f"Successfully upgraded to {plan_info['name']}!",
        "transaction_id": tx_id,
        "amount_charged": amount,
        "user": dict(updated_user)
    }

@router.post("/topup-credits")
def topup_credits(payload: AddCreditsRequest):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (payload.user_email,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
        
    tx_id = f"cred_{uuid.uuid4().hex[:16]}"
    cursor.execute("""
        INSERT INTO transactions (id, user_id, customer_email, product_id, amount, currency, provider, status)
        VALUES (?, ?, ?, 'credit_topup', ?, 'USD', 'stripe', 'completed')
    """, (tx_id, user["id"], user["email"], payload.cost_usd))
    
    cursor.execute("""
        UPDATE users SET credits = credits + ? WHERE id = ?
    """, (payload.amount_credits, user["id"]))
    
    conn.commit()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user["id"],))
    updated_user = cursor.fetchone()
    conn.close()
    
    return {
        "status": "success",
        "message": f"Added {payload.amount_credits} credits.",
        "user": dict(updated_user)
    }
