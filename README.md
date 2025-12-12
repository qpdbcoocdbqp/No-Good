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
cd remote-offline-store/offline_server
feast -c feature_repo apply
feast -c feature_repo serve_offline
```

* run client
```sh
cd remote-offline-store/offline_client
python test.py
```

* down server
```sh
feast -c feature_repo teardown
```

### **Credit risk**

```sh
cd credit-risk-end-to-end
uv pip install -r requirements.txt

```
Review

- [x] `01_Credit_Risk_Data_Prep`
- [x] `02_Deploying_the_Feature_Store`
- [ ] `03_Credit_Risk_Model_Training`
- [ ] `04_Credit_Risk_Model_Serving`
- [ ] `05_Credit_Risk_Cleanup`