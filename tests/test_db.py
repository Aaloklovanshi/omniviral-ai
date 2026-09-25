import sys
from pathlib import Path
import uuid

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.database import get_connection, init_db

def test_db_operations():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Test User Queries
    cursor.execute("SELECT * FROM users WHERE email = 'freeediting35@gmail.com'")
    user = cursor.fetchone()
    assert user is not None
    assert user["plan"] == "agency"
    print("✓ User query verified")
    
    # 2. Test Digital Products Count
    cursor.execute("SELECT COUNT(*) FROM digital_products")
    prod_count = cursor.fetchone()[0]
    assert prod_count >= 4
    print(f"✓ Products table verified ({prod_count} records)")
    
    # 3. Test Transaction Insertion
    tx_id = f"test_{uuid.uuid4().hex[:12]}"
    cursor.execute("""
        INSERT INTO transactions (id, user_id, customer_email, product_id, amount, currency, provider, status)
        VALUES (?, ?, 'test@creator.io', 'plan_pro', 49.00, 'USD', 'stripe', 'completed')
    """, (tx_id, user["id"]))
    conn.commit()
    
    cursor.execute("SELECT * FROM transactions WHERE id = ?", (tx_id,))
    tx = cursor.fetchone()
    assert tx is not None
    assert tx["amount"] == 49.00
    print("✓ Transaction insertion & commit verified")
    
    conn.close()

if __name__ == "__main__":
    test_db_operations()
    print("\n🎉 ALL DATABASE INTEGRITY TESTS PASSED!")
