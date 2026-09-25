from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from backend.database import get_connection

router = APIRouter(prefix="/api/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    name: Optional[str] = "Creator"

@router.post("/login")
def login_or_register(payload: LoginRequest):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE email = ?", (payload.email,))
    user = cursor.fetchone()
    
    if not user:
        user_id = str(uuid.uuid4())
        api_key = f"ov_{uuid.uuid4().hex[:24]}"
        cursor.execute("""
            INSERT INTO users (id, email, name, plan, credits, api_key)
            VALUES (?, ?, ?, 'free', 100, ?)
        """, (user_id, payload.email, payload.name, api_key))
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
    user_dict = dict(user)
    conn.close()
    return {"status": "success", "user": user_dict}

@router.get("/me")
def get_current_user(email: str = "freeediting35@gmail.com"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "user": dict(user)}
