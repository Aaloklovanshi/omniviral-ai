import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from agents.orchestrator import run_20_agent_swarm
from backend.database import get_connection

def test_swarm_execution():
    results = run_20_agent_swarm(parallel_workers=20)
    assert len(results) == 20
    print(f"✓ Verified 20/20 autonomous agent swarm execution")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM agent_runs")
    count = cursor.fetchone()[0]
    assert count >= 20
    print(f"✓ Verified database persistence ({count} agent task logs stored)")
    conn.close()

if __name__ == "__main__":
    test_swarm_execution()
    print("\n🎉 ALL AGENT SWARM TESTS PASSED!")
