import os
import random
import traceback
from pathlib import Path
import pyarrow as pa
import vortex as vx
import vortex.expr as ve

# Define the output directory
OUTPUT_DIR = Path("./output/example/vortex")

def setup_directory():
    """Ensure the output directory exists."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def basic_write_read():
    """Basic write and read operations."""
    print("=== Basic Write and Read ===")
    
    # Create a simple array
    data = vx.array([1, 2, 3, 4, 5, None, 7, 8, 9, 10])
    file_path = OUTPUT_DIR / "simple.vortex"
    
    # Write to file
    vx.io.write(data, str(file_path))
    print(f"✓ Written to {file_path}")
    
    # Read from file
    vxf = vx.open(str(file_path))
    result = vxf.scan().read_all()
    print(f"Read result: {result.to_arrow_array()}")
    print()

def struct_data_example():
    """Structured data example."""
    print("=== Structured Data ===")
    
    # Create structured data
    people = vx.array([
        {'name': 'Alice', 'age': 30, 'city': 'Taipei'},
        {'name': 'Bob', 'age': 25, 'city': 'Taichung'},
        {'name': None, 'age': 35, 'city': 'Kaohsiung'},
        {'name': 'David', 'age': None, 'city': 'Tainan'},
        {'name': 'Eve', 'age': 28, 'city': None},
    ])
    
    file_path = OUTPUT_DIR / "people.vortex"
    
    # Write to file
    vx.io.write(people, str(file_path))
    print(f"✓ Written to {file_path}")
    
    # Read all data
    vxf = vx.open(str(file_path))
    all_data = vxf.scan().read_all().to_arrow_array()
    print(f"All data:\n{all_data}")
    print()

def projection_example():
    """Projection (selecting specific columns) example."""
    print("=== Projection Example ===")
    
    file_path = OUTPUT_DIR / "people.vortex"
    vxf = vx.open(str(file_path))
    
    # Read only the 'name' column
    names = vxf.scan(['name']).read_all().to_arrow_array()
    print(f"Read 'name' only:\n{names}")
    
    # Read only the 'age' column
    ages = vxf.scan(['age']).read_all().to_arrow_array()
    print(f"Read 'age' only:\n{ages}")
    print()

def filtering_example():
    """Filtering data example."""
    print("=== Filtering Example ===")
    
    file_path = OUTPUT_DIR / "people.vortex"
    vxf = vx.open(str(file_path))
    
    # Filter for age > 27
    filtered = vxf.scan(expr=ve.column("age") > 27).read_all().to_arrow_array()
    print(f"Age > 27:\n{filtered}")
    print()

def compression_comparison():
    """Compression comparison example."""
    print("=== Compression Comparison ===")
    
    # Create large dataset
    large_data = vx.array([random.randint(i, i + 10) for i in range(10000)])
    
    default_path = OUTPUT_DIR / "default.vortex"
    compact_path = OUTPUT_DIR / "compact.vortex"
    
    # Write with default settings
    vx.io.VortexWriteOptions.default().write(large_data, str(default_path))
    default_size = os.path.getsize(default_path)
    print(f"Default compression size: {default_size:,} bytes")
    
    # Write with compact settings (priority on file size)
    vx.io.VortexWriteOptions.compact().write(large_data, str(compact_path))
    compact_size = os.path.getsize(compact_path)
    print(f"Compact compression size: {compact_size:,} bytes")
    print(f"Compression ratio: {compact_size / default_size:.2%}")
    print()

def repeated_scan_example():
    """Repeated scan example (ideal for multiple reads from the same file)."""
    print("=== Repeated Scan Example ===")
    
    file_path = OUTPUT_DIR / "people.vortex"
    vxf = vx.open(str(file_path))
    
    # Prepare a reusable scan
    scan = vxf.to_repeated_scan()
    
    # Execute multiple scans on different ranges
    range1 = scan.execute(row_range=(0, 2)).read_all().to_arrow_array()
    print(f"Rows 0-2:\n{range1}")
    
    range2 = scan.execute(row_range=(2, 4)).read_all().to_arrow_array()
    print(f"Rows 2-4:\n{range2}")
    
    # Get scalar value at specific index
    scalar = scan.scalar_at(1)
    print(f"Value at index 1: {scalar}")
    print()

def arrow_integration():
    """Integration with PyArrow example."""
    print("=== PyArrow Integration ===")
    
    # Create data from PyArrow Table
    table = pa.table({
        'id': [1, 2, 3, 4, 5],
        'value': [10.5, 20.3, 30.1, 40.8, 50.2],
        'label': ['A', 'B', 'C', 'D', 'E']
    })
    
    file_path = OUTPUT_DIR / "from_arrow.vortex"
    vx.io.write(table, str(file_path))
    print(f"✓ Written from PyArrow Table to {file_path}")
    
    # Read as PyArrow RecordBatchReader
    vxf = vx.open(str(file_path))
    reader = vxf.to_arrow()
    
    for batch in reader:
        print(f"RecordBatch (to Pandas for display):\n{batch.to_pandas()}")
    print()

# Additional examples for multi-file datasets and schema evolution
def multi_file_dataset_example(conn):
    """Example of handling multiple Vortex files as a single dataset."""
    print("=== Multi-file Dataset ===")
    
    dataset_dir = OUTPUT_DIR / "multi_part_dataset"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    
    # Create two different partitions
    part1 = vx.array([{'id': 1, 'val': 'A'}, {'id': 2, 'val': 'B'}])
    part2 = vx.array([{'id': 3, 'val': 'C'}, {'id': 4, 'val': 'D'}])
    
    vx.io.write(part1, str(dataset_dir / "part1.vortex"))
    vx.io.write(part2, str(dataset_dir / "part2.vortex"))
    print(f"✓ Written two partitions to {dataset_dir}")

    # Count total rows across the directory
    print(f"\nScanning directory {str(dataset_dir)}")
    import duckdb
    conn = duckdb.connect()
    conn.execute("INSTALL vortex; LOAD vortex;")
    result = conn.execute(f"SELECT COUNT(*) FROM vortex_scan('{dataset_dir}/*.vortex')").fetchone()
    total_rows = result[0] if result else 0
    print(f"Total rows in dataset: {total_rows}")
    print()

def schema_evolution_example(conn):
    """Example of schema evolution (merging different column sets)."""
    print("=== Schema Evolution ===")
    
    evolution_dir = OUTPUT_DIR / "evolution"
    evolution_dir.mkdir(parents=True, exist_ok=True)
    
    # Version 1: Basic info
    v1_data = vx.array([
        {'id': 101, 'name': 'Alpha'}
    ])
    
    # Version 2: New column 'status' added
    v2_data = vx.array([
        {'id': 102, 'name': 'Beta', 'status': 'active'}
    ])
    
    vx.io.write(v1_data, str(evolution_dir / "v1.vortex"))
    vx.io.write(v2_data, str(evolution_dir / "v2.vortex"))
    
    # Vortex handles the union of schemas automatically when scanning the directory
    # Missing columns in older files are typically filled with nulls
    result = conn.execute(f"SELECT * FROM vortex_scan('{evolution_dir}/*.vortex')").df()
    print(f"Evolved Schema Result:\n{result}")
    print("Notice: 'status' for ID 101 is null as it didn't exist in v1.")
    print()

def main():
    """Execute all examples."""
    try:
        setup_directory()
        
        # basic examples
        basic_write_read()
        struct_data_example()
        projection_example()
        filtering_example()
        compression_comparison()
        repeated_scan_example()
        arrow_integration()

        # Additional examples
        import duckdb
        conn = duckdb.connect()
        conn.execute("INSTALL vortex; LOAD vortex;")

        multi_file_dataset_example(conn)
        schema_evolution_example(conn)

        print("✓ All examples executed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()