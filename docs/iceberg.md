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