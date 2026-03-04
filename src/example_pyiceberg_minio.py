from pyiceberg.catalog import load_catalog
import pandas as pd
import pyarrow as pa

# 1. Load a local SQL catalog (using SQLite) but configure MinIO for S3 storage
# Note: You need to install pyiceberg with s3fs support (e.g. `uv pip install "pyiceberg[pyarrow,pandas,s3fs]"`)
# Ensure the bucket 'iceberg-warehouse' exists in your MinIO instance.
catalog = load_catalog("minio_catalog", **{
    "type": "sql",
    "uri": "sqlite:///./iceberg_minio_catalog.db",
    "warehouse": "s3://iceberg-warehouse",
    "s3.endpoint": "http://localhost:9000",
    "s3.access-key-id": "minioadmin",        # Default MinIO credentials
    "s3.secret-access-key": "minioadmin",    # Default MinIO credentials
    "s3.region": "us-east-1",                # MinIO usually needs a default region
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
