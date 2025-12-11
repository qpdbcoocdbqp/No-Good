# No-Good
Run a feature store. Playing with [No Good](https://www.youtube.com/watch?v=HC6QJsxRypQ).

* **About No Good**

> No Good ·KALEO
> 
> A/B

## Reference
* [feast](https://github.com/feast-dev/feast)

## Explore
* **Setup**
```sh
uv venv --python 3.12
uv pip install feast
```

### **Quickstart**

From [quickstart](https://github.com/feast-dev/feast/tree/master/examples/quickstart)

```sh
source .venv/bin/activate
feast init feature_repo
cd feature_repo/feature_repo
python -m test_workflow
```

### **Remote offline store**

From [remote-offline-store](https://github.com/feast-dev/feast/tree/master/examples/remote-offline-store)

* start server
```sh
cd offline_server
feast -c feature_repo apply
feast -c feature_repo serve_offline
```

* run client
```sh
cd offline_client
python test.py
```

* down server
```sh
feast -c feature_repo teardown
```