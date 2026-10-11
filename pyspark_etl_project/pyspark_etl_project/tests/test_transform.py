from pyspark.sql import SparkSession
from src.transform import clean_sales


def test_clean_sales_splits_invalid_quantity():
    spark = (
        SparkSession.builder
        .master("local[1]")
        .appName("test-transform")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    try:
        rows = [
            ("1", "2026-01-01", "C1", "P1", 2, 3.0),
            ("2", "2026-01-01", "C2", "P1", 0, 3.0),
        ]
        columns = ["sale_id", "order_date", "customer_id", "product_id", "quantity", "unit_price"]
        df = spark.createDataFrame(rows, columns)
        valid, rejected = clean_sales(df)
        assert valid.count() == 1
        assert rejected.count() == 1
        assert rejected.first()["rejection_reason"] == "non_positive_quantity"
    finally:
        spark.stop()
