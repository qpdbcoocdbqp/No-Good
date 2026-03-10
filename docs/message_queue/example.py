import os
import time
from celery import Celery

# Celery Configuration
# In Docker, 'localhost' should be replaced by the service name (e.g., 'redis')
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

app = Celery('example', 
             broker=REDIS_URL, 
             backend=REDIS_URL)

@app.task(name='example.send_email')
def send_email(user_email):
    """
    A sample task that simulates sending an email.
    """
    print(f"Simulating sending email to {user_email}...")
    time.sleep(3)  # Simulate network delay/processing time
    return f"Email sent to {user_email} successfully!"

if __name__ == "__main__":
    # This block demonstrates how to CALL the task from your code
    print("--- Celery Task Example ---")
    
    user = "demo@example.com"
    print(f"1. Dispatching task for user: {user}")
    
    # .delay() is a shortcut to .apply_async()
    result = send_email.delay(user)
    
    print(f"2. Task ID: {result.id}")
    print("3. Waiting for worker to process... (Check your Celery worker console)")
    
    try:
        # .get() will block until the result is ready
        output = result.get(timeout=10)
        print(f"4. Result received: {output}")
    except Exception as e:
        print(f"Error or timeout: {e}")
        print("\nNote: Make sure you have a Redis server running and a Celery worker:")
        print("Run worker: celery -A example worker --loglevel=info -P solo")
