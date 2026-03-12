# Research message queue (python)

**Reference**

* [celery/celery](https://github.com/celery/celery)
* [rq/rq](https://github.com/rq/rq)
* [RabbitMQ](https://github.com/rabbitmq/rabbitmq-website)

## Celery Usage Example

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

4. **Run RabbitMQ example**:
   ```bash
   # In terminal 1 (Consumer)
   docker-compose exec app python rabbitmq_example.py consumer
   
   # In terminal 2 (Producer)
   docker-compose exec app python rabbitmq_example.py producer "Hello Rabbit!"
   ```

5. **Show logs**:
   * **Celery**: `docker-compose logs -f worker`
   * **RQ**: `docker-compose logs -f rq-worker`
   * **RabbitMQ**: `docker-compose logs -f rabbitmq`

## RabbitMQ Usage Example

Refer to [rabbitmq_example.py](rabbitmq_example.py) for a basic setup using the `pika` library.

### Steps to Run

1. **Install dependencies**:
   ```bash
   uv pip install pika
   ```

2. **Start RabbitMQ** (using Docker):
   ```bash
   docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management
   ```

3. **Run the Consumer**:
   ```bash
   python rabbitmq_example.py consumer
   ```

4. **Trigger the Producer**:
   ```bash
   python rabbitmq_example.py producer "Message via RabbitMQ"
   ```


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
