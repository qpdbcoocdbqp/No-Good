# Vortex

**Reference**

* [vortex-data/vortex](https://github.com/vortex-data/vortex/tree/develop)

* [python API - docs](https://docs.vortex.dev/api/python/io)

## Setup

* python install package

    ```sh
    uv venv --python 3.13
    uv pip install vortex-data duckdb pyarrow
    ```

## Example

* create simple vortex

    ```sh
    source ~/.venv/bin/activate
    python -m src.example_vortex
    ```

    The `src/example_vortex.py` script demonstrates the following features of the Vortex library:

    *   **Basic Write/Read**: Simple data persistence and retrieval using `vx.io.write` and `vx.open`.
    *   **Structured Data**: Support for nested structures and null values within arrays.
    *   **Projection**: Efficiently reading only specific columns from a file.
    *   **Filtering**: Using `vortex.expr` to perform server-side (or engine-side) row filtering.
    *   **Compression Options**: Comparing `default` vs. `compact` write options to balance speed and file size.
    *   **Repeated Scans**: Utilizing `to_repeated_scan()` for optimized, reusable scan objects, including random access via `scalar_at`.
    *   **PyArrow Integration**: Seamless conversion between Vortex files and PyArrow Tables/RecordBatchReaders.
    *   **Multi-file Datasets**: Scanning directories of Vortex files as a single logical dataset using the DuckDB extension.
    *   **Schema Evolution**: Demonstrating how Vortex (via DuckDB) handles files with differing schemas by automatically merging columns.
