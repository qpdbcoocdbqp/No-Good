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