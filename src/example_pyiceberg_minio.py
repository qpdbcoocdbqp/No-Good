from pyiceberg.catalog import load_catalog
import pandas as pd
import pyarrow as pa
import socket

# Monkeypatch socket.getaddrinfo to resolve "minio" to 127.0.0.1
# This is necessary because the Lakekeeper REST catalog returns properties
# specifying "http://minio:9000" and overrides local catalog settings.
_old_getaddrinfo = socket.getaddrinfo
def _new_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    if host == "minio":
        host = "127.0.0.1"
    return _old_getaddrinfo(host, port, family, type, proto, flags)
socket.getaddrinfo = _new_getaddrinfo

# 1. Load a catalog.
# Option A: Local SQL catalog (using SQLite) but configure MinIO for S3 storage
# Note: You need to install pyiceberg with s3fs support (e.g. `uv pip install "pyiceberg[pyarrow,pandas,s3fs]"`)
# Ensure the bucket 'iceberg-warehouse' exists in your MinIO instance.
# catalog = load_catalog("minio_catalog", **{
#     "type": "sql",
#     "uri": "sqlite:///./iceberg_minio_catalog.db",
#     "warehouse": "s3://iceberg-warehouse",
#     "s3.endpoint": "http://localhost:9000",
#     "s3.access-key-id": "minioadmin",        # Default MinIO credentials
#     "s3.secret-access-key": "minioadmin",    # Default MinIO credentials
#     "s3.region": "us-east-1",                # MinIO usually needs a default region
# })

# Option B: Lakekeeper REST catalog (requires a running Lakekeeper server)
catalog = load_catalog("lakekeeper", **{
    "type": "rest",
    "uri": "http://localhost:8181/catalog",
    "warehouse": "whs",
    "s3.endpoint": "http://localhost:9000",
    "client.s3.endpoint": "http://localhost:9000",
    "s3.access-key-id": "minioadmin",
    "s3.secret-access-key": "minioadmin",
    "s3.region": "us-east-1",
})


# 2. Create a namespace
catalog.create_namespace_if_not_exists("default")

# 3. Define a schema (Using PyArrow)
schema = pa.schema([
    pa.field("id", pa.int32(), nullable=False),
    pa.field("name", pa.string(), nullable=True),
])

# 4. Create or load a table
identifier = "default.users_minio"
try:
    table = catalog.load_table(identifier)
except:
    table = catalog.create_table(identifier, schema=schema)

# 5. Append data using a Pandas DataFrame
df = pd.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"]})
# Cast to int32 to match Iceberg 'int' (32-bit) schema
df["id"] = df["id"].astype("int32") 
# Use the defined schema to ensure nullability (required vs optional) matches
table.append(pa.Table.from_pandas(df, schema=schema))

# 6. Read and display data
print(table.scan().to_pandas())

# Append more data
df2 = pd.DataFrame({"id": [5, 6, 7], "name": ["David", "Eve", "Frank"]})
df2["id"] = df2["id"].astype("int32") 
table.append(pa.Table.from_pandas(df2, schema=schema))
print("\nAfter Append:")
print(table.scan().to_pandas())

# 7. Update data (Overwrite specific rows by replacing them)
# For example, let's update id=5's name from "David" to "David (Updated)"
df_update = pd.DataFrame({"id": [5], "name": ["David (Updated)"]})
df_update["id"] = df_update["id"].astype("int32") 
table.overwrite(pa.Table.from_pandas(df_update, schema=schema), overwrite_filter="id == 5")
print("\nAfter Update (Overwrite id == 5):")
print(table.scan().to_pandas())

# 8. Delete data (Row-level delete based on boolean expression)
# For example, let's delete id=6
table.delete(delete_filter="id == 6")
print("\nAfter Delete (id == 6):")
print(table.scan().to_pandas())

