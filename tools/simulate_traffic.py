import requests
import random
import time
import threading
import psycopg2
import os

# ================================================================
# CONFIGURATION
# ================================================================

BASE = "http://web:8000"   # inside Docker network

RUN_SECONDS = 120
APP_THREADS = 40
DB_THREADS = 5

# ================================================================
# DATABASE CONFIG (from docker env)
# ================================================================

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST", "db"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}

# ================================================================
# TRAFFIC DISTRIBUTION (Weighted)
# ================================================================

ENDPOINTS = [
    ("/observability/meetings/", 0.5),
    ("/observability/messages/", 0.3),
    ("/health/", 0.2),
]

def choose_endpoint():
    paths = [e[0] for e in ENDPOINTS]
    weights = [e[1] for e in ENDPOINTS]
    return random.choices(paths, weights=weights)[0]

# ================================================================
# PAYLOAD GENERATORS
# ================================================================

def random_meeting_data():
    return {
        "title": f"Team Sync {random.randint(1, 10000)}",
        "scheduled_at": "2025-11-03T12:00:00Z",
        "created_by": 1
    }

def random_message_data():
    return {
        "meeting": random.randint(1, 5),
        "sender": 1,
        "content": f"Message {random.randint(1, 10000)}"
    }

# ================================================================
# APPLICATION LOAD
# ================================================================

def app_worker(stop_time):
    while time.time() < stop_time:

        path = choose_endpoint()
        url = BASE + path

        try:
            if "meetings" in path:
                if random.random() < 0.6:
                    requests.post(url, json=random_meeting_data(), timeout=5)
                else:
                    requests.get(url, timeout=5)

            elif "messages" in path:
                if random.random() < 0.7:
                    requests.post(url, json=random_message_data(), timeout=5)
                else:
                    requests.get(url, timeout=5)

            else:
                requests.get(url, timeout=5)

        except Exception:
            pass

        time.sleep(random.uniform(0.01, 0.05))

# ================================================================
# DATABASE LOAD
# ================================================================

def db_worker(stop_time):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        while time.time() < stop_time:
            q = random.choice([
                "SELECT 1;",
                "SELECT now();",
                "SELECT generate_series(1, 500);",
                "SELECT pg_sleep(0.02);"
            ])
            cur.execute(q)
            conn.commit()
            time.sleep(random.uniform(0.05, 0.15))

        cur.close()
        conn.close()

    except Exception:
        pass

# ================================================================
# MAIN
# ================================================================

if __name__ == "__main__":

    print(f"\n🚀 Starting traffic simulation")
    print(f"App threads: {APP_THREADS}")
    print(f"DB threads: {DB_THREADS}")
    print(f"Duration: {RUN_SECONDS} seconds\n")

    stop_time = time.time() + RUN_SECONDS

    threads = []

    # Application load threads
    for _ in range(APP_THREADS):
        t = threading.Thread(target=app_worker, args=(stop_time,))
        t.start()
        threads.append(t)

    # DB load threads
    for _ in range(DB_THREADS):
        t = threading.Thread(target=db_worker, args=(stop_time,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("\n✅ Simulation complete.")
    print("👉 Check Grafana dashboards.\n")