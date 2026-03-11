import time

def send_message(name):
    """
    A simple task that simulates a background process.
    """
    print(f"RQ: Processing message for {name}...")
    time.sleep(2)
    return f"Hello, {name}! Task completed."
