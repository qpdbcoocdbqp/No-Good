# Iceberg

**Reference**

* GitHub: [apache/iceberg-python](https://github.com/apache/iceberg-python)
* Documentation: [PyIceberg Documentation](https://pyiceberg.apache.org/)


## Setup

* python install package

    ```sh
    uv venv --python 3.13
    # On Windows:
    # .venv\Scripts\activate
    uv pip install "pyiceberg[pyarrow,pandas]"
    ```


## Example

* create iceberg table and write data

  ```sh
  python src/example_pyiceberg.py
  ```

  * output

  ```
  id  name
  0   1 Alice
  1   2   Bob
  2   3 Charlie
  ```

## MinIO Example

* To use MinIO (S3-compatible storage) as the backend warehouse, first install s3fs:

  ```sh
  uv pip install "pyiceberg[pyarrow,pandas,s3fs]"
  ```

* Ensure MinIO is running locally (`http://localhost:9000`) and the `iceberg-warehouse` bucket exists. Then evaluate the S3 example:

  ```sh
  python src/example_pyiceberg_minio.py
  ```

* MinIO

  ```sh
  docker pull minio/minio:latest
  docker run -d \
  -p 9000:9000 -p 9001:9001 \
  -v ./minio_data:/data \
  --name minio \
  minio/minio:latest server /data --console-address ":9001"
  ```
  * MinIO Console: `http://localhost:9001`
  * Default MinIO user / password: `minioadmin` / `minioadmin`
  * Make sure create bucket `iceberg-warehouse`

## Lakekeeper (REST Catalog)

[Lakekeeper](https://lakekeeper.io/) is an Apache-licensed Apache Iceberg REST Catalog.

### Using Docker Compose (Recommended)

Since Lakekeeper requires PostgreSQL as a database, we have configured automated database persistence and migrations in `docker-compose.yaml`:

1. **Start all services**:
   ```sh
   docker compose up -d
   ```

This will automatically perform the following:
*   **PostgreSQL**: Starts and persists data to the `./postgres_data` subdirectory.
*   **Lakekeeper Migrate**: Automatically detects and executes database migrations.
*   **Lakekeeper Setup**: Automatically creates a Storage Profile and initializes a warehouse named `whs`.
*   **Lakekeeper Server**: Starts the REST Catalog service at `http://localhost:8181`.
*   **MinIO**: Starts the S3 API (`:9000`) and Console (`:9001`).

*After starting, ensure you create the `iceberg-warehouse` bucket in MinIO.*

### Manual Docker Setup (If database already exists)

If you already have a running PostgreSQL instance:


```sh
docker run -d \
  -p 8181:8181 \
  -e "LAKEKEEPER__PG_DATABASE_URL_WRITE=postgres://[user]:[password]@[host]:5432/[db]" \
  --name lakekeeper \
  quay.io/lakekeeper/catalog:latest serve
```

### PyIceberg Configuration

To connect `pyiceberg` to Lakekeeper, use the following configuration. 

**Note on host resolution**: Since Lakekeeper may return the internal Docker hostname `minio` in storage properties, you might need to monkeypatch `socket.getaddrinfo` if you are running the script outside the Docker network.

```python
import socket
from pyiceberg.catalog import load_catalog

# Monkeypatch socket.getaddrinfo to resolve "minio" to 127.0.0.1
_old_getaddrinfo = socket.getaddrinfo
def _new_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    if host == "minio":
        host = "127.0.0.1"
    return _old_getaddrinfo(host, port, family, type, proto, flags)
socket.getaddrinfo = _new_getaddrinfo

catalog = load_catalog("lakekeeper", **{
    "type": "rest",
    "uri": "http://localhost:8181/catalog",
    "warehouse": "whs",                      # Ensure this matches your warehouse name
    "s3.endpoint": "http://localhost:9000",
    "client.s3.endpoint": "http://localhost:9000",
    "s3.access-key-id": "minioadmin",
    "s3.secret-access-key": "minioadmin",
    "s3.region": "us-east-1",
})
```

You can find the full working example in [example_pyiceberg_minio.py](../src/example_pyiceberg_minio.py).

* **Expected Output**:

  ```text
     id     name
  0   1    Alice
  1   2      Bob
  2   3  Charlie
  
  After Append:
     id     name
  0   1    Alice
  1   2      Bob
  2   3  Charlie
  3   5    David
  4   6      Eve
  5   7    Frank
  
  After Update (Overwrite id == 5):
     id             name
  0   1            Alice
  1   2              Bob
  2   3          Charlie
  3   6              Eve
  4   7            Frank
  5   5  David (Updated)
  
  After Delete (id == 6):
     id             name
  0   1            Alice
  1   2              Bob
  2   3          Charlie
  3   7            Frank
  4   5  David (Updated)
  ```

### Data Manipulation: Update and Delete

With recent versions of PyIceberg (using PyArrow), manipulating row-level data is supported. Lakekeeper (REST Catalog) perfectly handles these metadata updates.

* **Update**
  Use `overwrite()` paired with an `overwrite_filter` to apply modifications. This performs a row-level update on elements that match the filter.
  
  ```python
  # Update id=5's name from "David" to "David (Updated)"
  df_update = pd.DataFrame({"id": [5], "name": ["David (Updated)"]})
  df_update["id"] = df_update["id"].astype("int32") 
  table.overwrite(pa.Table.from_pandas(df_update, schema=schema), overwrite_filter="id == 5")
  ```

* **Delete**
  Use `delete()` with a `delete_filter` to permanently remove rows based on specific conditions. PyIceberg leverages expressions to handle conditional deletions correctly.

  ```python
  # Row-level delete based on boolean expression
  table.delete(delete_filter="id == 6")
  ```

You can view the full script implementation inside [`src/example_pyiceberg_minio.py`](../src/example_pyiceberg_minio.py).
