from pyiceberg.catalog import load_catalog
import pandas as pd
import pyarrow as pa

# 1. Load a local SQL catalog (using SQLite)
catalog = load_catalog("local", **{
    "type": "sql",
    "uri": "sqlite:///./iceberg_catalog.db",
    "warehouse": "./warehouse",
})

# 2. Create a namespace
catalog.create_namespace_if_not_exists("default")

# 3. Define a schema (Using PyArrow)
schema = pa.schema([
    pa.field("id", pa.int32(), nullable=False),
    pa.field("name", pa.string(), nullable=True),
])

# 4. Create or load a table
identifier = "default.users"
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
