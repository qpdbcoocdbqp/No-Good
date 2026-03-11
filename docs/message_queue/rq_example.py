import os
import time
from redis import Redis
from rq import Queue
from tasks import send_message

# Redis Configuration
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
redis_conn = Redis.from_url(REDIS_URL)
q = Queue(connection=redis_conn)

if __name__ == "__main__":
    print("--- RQ Task Example ---")
    
    name = "World"
    print(f"1. Enqueueing task for: {name}")
    
    # Enqueue the task from the 'tasks' module
    job = q.enqueue(send_message, name)
    
    print(f"2. Job ID: {job.id}")
    print("3. Waiting for worker to process... (Check your RQ worker console)")
    
    # Polling for result
    retries = 15
    while retries > 0:
        job.refresh() # Update job status from Redis
        if job.is_finished:
            print(f"4. Result received: {job.result}")
            break
        elif job.is_failed:
            print("4. Job failed.")
            break
        time.sleep(1)
        retries -= 1
    else:
        print("Timeout waiting for result. Ensure a worker is running.")
        print("\nNote: Make sure you have a Redis server running and an RQ worker:")
        print(f"Run worker: rq worker --url {REDIS_URL}")
