import pyarrow as pa
import vortex as vx
from pathlib import Path


# Define the output directory
OUTPUT_DIR = Path("./output/example/iceberg_vortex")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def iceberg_vortex_example():
    """
    Example showing how Vortex files can be used within an Iceberg context.
    Note: Native Iceberg write support for Vortex is emerging. 
    This example shows the interoperability via PyArrow.
    """
    print("=== Iceberg & Vortex Interoperability ===")
    
    # 1. Create a PyArrow Table (common format for Iceberg)
    table = pa.table({
        'id': [1, 2, 3, 4, 5],
        'name': ['Item A', 'Item B', 'Item C', 'Item D', 'Item E'],
        'value': [10.5, 20.0, 15.2, 30.1, 25.4]
    })
    
    # 2. Write as Vortex file
    # In an Iceberg table, Vortex can be used as the storage format for data files.
    vortex_file = OUTPUT_DIR / "data_file.vortex"
    vx.io.write(table, str(vortex_file))
    print(f"✓ Data written to Vortex file: {vortex_file}")
    
    # 3. Reading back (Simulating Iceberg scanning a Vortex data file)
    vxf = vx.open(str(vortex_file))
    
    # We can use projections and filters just like Iceberg would
    # Read only id and value where value > 20.0
    import vortex.expr as ve
    result = vxf.scan(['id', 'value'], expr=ve.column("value") > 20.0).read_all()
    
    print(f"Filtered result from Vortex file:{result.to_arrow_table()}")
    
    # 4. Converting to PyArrow for Iceberg metadata integration
    # Iceberg's Python API (pyiceberg) works with PyArrow.
    # You can easily convert a Vortex scan result back to Arrow.
    arrow_table = vxf.scan().read_all().to_arrow_table()
    print(f"Successfully converted Vortex data back to PyArrow Table (Size: {len(arrow_table)} rows)")
    print()

if __name__ == "__main__":
    try:
        iceberg_vortex_example()
        print("✓ Iceberg-Vortex example executed successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
