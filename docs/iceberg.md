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

### 使用 Docker Compose 啟動 (推薦)

由於 Lakekeeper 需要 PostgreSQL 作為資料庫，我們在 `docker-compose.yaml` 中配置了自動化的資料庫持久化和遷移：

1. **啟動所有服務**:
   ```sh
   docker compose up -d
   ```

這會自動完成以下工作：
*   **PostgreSQL**: 啟動並將資料持久化到 `./postgres_data` 子目錄。
*   **Lakekeeper Migrate**: 自動檢測並執行資料庫遷移（Migration）。
*   **Lakekeeper Setup**: 自動建立 Storage Profile 並初始化一個名為 `demo` 的 Warehouse。
*   **Lakekeeper Server**: 啟動 REST Catalog 服務，網址為 `http://localhost:8181`。
*   **MinIO**: 啟動 S3 API (`:9000`) 與控制台 (`:9001`)。

*啟動後，請確保在 MinIO 中建立 `iceberg-warehouse` bucket。*

### 手動使用 Docker 啟動 (若已有資料庫)

如果您已經有運作中的 PostgreSQL：

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

  ```
     id     name
  0   1    Alice
  1   2      Bob
  2   3  Charlie

     id     name
  0   1    Alice
  1   2      Bob
  2   3  Charlie
  3   5    David
  4   6      Eve
  5   7    Frank
  ```
