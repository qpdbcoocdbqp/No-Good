# Research message queue (python)

**Reference**

* [celery/celery](https://github.com/celery/celery)
* [rq](https://github.com/rq/rq)

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

Use Docker Compose (Redis, Celery Worker, RQ Worker).

1. **Start services**:
   ```bash
   docker-compose up --build -d
   ```

2. **Run Celery example**:
   ```bash
   docker-compose exec app python example.py
   ```

3. **Run RQ example**:
   ```bash
   docker-compose exec app python rq_example.py
   ```

4. **Show logs**:
   * **Celery**: `docker-compose logs -f worker`
   * **RQ**: `docker-compose logs -f rq-worker`


## RQ Usage Example

Refer to [rq_example.py](rq_example.py) for a basic setup using Redis.

### Steps to Run

1. **Install dependencies**:
   ```bash
   uv pip install rq redis
   ```

2. **Start Redis** (if not already running):
   ```bash
   docker run -d -p 6379:6379 redis
   ```

3. **Run the RQ Worker**:
   > [!IMPORTANT]
   > RQ Worker does not support Windows natively because it requires `fork()`. 
   > For Windows users, please use **Docker** or **WSL2** to run the worker.

   ```bash
   # (Linux/macOS/Docker only)
   rq worker --url redis://localhost:6379/0
   ```

4. **Trigger the Task**:
   ```bash
   python rq_example.py
   ```
