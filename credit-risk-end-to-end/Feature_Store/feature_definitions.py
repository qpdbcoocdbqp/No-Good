
# Imports
import os
from pathlib import Path
from feast import (
    FileSource,
    Entity,
    FeatureView,
    Field,
    FeatureService
)
from feast.types import Float32, String
from feast.data_format import ParquetFormat

# Data Sources
# A data source tells Feast where the data lives
data_a = FileSource(
    file_format=ParquetFormat(),
    path="data/data_a.parquet"
)
data_b = FileSource(
    file_format=ParquetFormat(),
    path="data/data_b.parquet"
)

# Entity
# An entity tells Feast the column it can use to join tables
loan_id = Entity(
    name = "loan_id",
    join_keys = ["ID"]
)

# Feature views
# A feature view is how Feast groups features
features_a = FeatureView(
    name="data_a",
    entities=[loan_id],
    schema=[
        Field(name="checking_status", dtype=String),
        Field(name="duration", dtype=Float32),
        Field(name="credit_history", dtype=String),
        Field(name="purpose", dtype=String),
        Field(name="credit_amount", dtype=Float32),
        Field(name="savings_status", dtype=String),
        Field(name="employment", dtype=String),
        Field(name="installment_commitment", dtype=Float32),
        Field(name="personal_status", dtype=String),
        Field(name="other_parties", dtype=String),
    ],
    source=data_a
)
features_b = FeatureView(
    name="data_b",
    entities=[loan_id],
    schema=[
        Field(name="residence_since", dtype=Float32),
        Field(name="property_magnitude", dtype=String),
        Field(name="age", dtype=Float32),
        Field(name="other_payment_plans", dtype=String),
        Field(name="housing", dtype=String),
        Field(name="existing_credits", dtype=Float32),
        Field(name="job", dtype=String),
        Field(name="num_dependents", dtype=Float32),
        Field(name="own_telephone", dtype=String),
        Field(name="foreign_worker", dtype=String),
    ],
    source=data_b
)

# Feature Service
# a feature service in Feast represents a logical group of features
loan_fs = FeatureService(
    name="loan_fs",
    features=[features_a, features_b]
)
