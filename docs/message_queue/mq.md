# Research message queue (python)

**Reference**

* [celery/celery](https://github.com/celery/celery)

## Usage Example

Refer to [example.py](example.py) for a basic setup using Redis.

### Steps to Run

1. **Install dependencies**:
   ```bash
   uv pip install celery redis
   ```

2. **Start Redis** (using Docker as an example):
   ```bash
   docker run -d -p 6379:6379 redis
   ```

3. **Run the Celery Worker** (Windows argument `-P solo`):
   ```bash
   celery -A example worker --loglevel=info -P solo
   ```

4. **Trigger the Task**:
   ```bash
   python example.py
   ```

## Docker Deployment

Use Docker Compose（Redis, Worker）。

1. **Start service**：
   ```bash
   docker-compose up --build -d
   ```

2. **Run example in container**：
   ```bash
   docker-compose exec app python example.py
   ```

3. **Show logs in Worker**：
   ```bash
   docker-compose logs -f worker
   ```
