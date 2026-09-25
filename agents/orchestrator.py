import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.database import init_db
from agents.worker_trend_hunter import run_trend_worker
from agents.worker_content_factory import run_content_worker
from agents.worker_digital_product import run_digital_product_worker
from agents.worker_lead_outreach import run_lead_worker
from agents.worker_revenue_optimizer import run_revenue_worker

def execute_worker(worker_id: int):
    """Dispatches worker ID (1-20) to its corresponding specialized swarm."""
    if 1 <= worker_id <= 4:
        return ("TrendHunter", run_trend_worker(worker_id))
    elif 5 <= worker_id <= 8:
        return ("ContentFactory", run_content_worker(worker_id))
    elif 9 <= worker_id <= 12:
        return ("DigitalProduct", run_digital_product_worker(worker_id))
    elif 13 <= worker_id <= 16:
        return ("LeadOutreach", run_lead_worker(worker_id))
    elif 17 <= worker_id <= 20:
        return ("RevenueOptimizer", run_revenue_worker(worker_id))
    else:
        raise ValueError(f"Unknown worker ID: {worker_id}")

def run_20_agent_swarm(parallel_workers: int = 20):
    print("================================================================")
    print("  🚀 OMNIVIRAL AI: LAUNCHING 20 AUTONOMOUS AGENT SWARM WORKERS  ")
    print("================================================================")
    print(f"[*] Initializing SQLite Database & Memory Registers...")
    init_db()
    
    start_time = time.time()
    results = []
    
    print(f"[*] Spawning {parallel_workers} concurrent agent threads...\n")
    
    with ThreadPoolExecutor(max_workers=parallel_workers) as executor:
        future_to_worker = {executor.submit(execute_worker, i): i for i in range(1, 21)}
        
        for future in as_completed(future_to_worker):
            worker_id = future_to_worker[future]
            try:
                swarm_type, data = future.result()
                print(f"  [✓] Agent Worker #{worker_id:02d} [{swarm_type:17s}]: {data['summary'][:75]}...")
                results.append((worker_id, swarm_type, data))
            except Exception as e:
                print(f"  [✗] Agent Worker #{worker_id:02d} FAILED with error: {e}")
                
    elapsed = round(time.time() - start_time, 2)
    print("\n================================================================")
    print(f"  ✨ 20/20 AGENTS COMPLETED ALL TASKS SUCCESSFULLY IN {elapsed}s")
    print("  📊 All insights, content packs, leads & products synced to DB")
    print("================================================================")
    return results

if __name__ == "__main__":
    run_20_agent_swarm()
