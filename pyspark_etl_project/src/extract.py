from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, DoubleType
)
from .utils import resolve_path


SALES_SCHEMA = StructType([
    StructField("sale_id", StringType(), True),
    StructField("order_date", StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("product_id", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("unit_price", DoubleType(), True),
])

PRODUCTS_SCHEMA = StructType([
    StructField("product_id", StringType(), True),
    StructField("product_name", StringType(), True),
    StructField("category", StringType(), True),
])


def extract_sales(spark: SparkSession, relative_path: str) -> DataFrame:
    return (
        spark.read.option("header", True)
        .option("mode", "PERMISSIVE")
        .schema(SALES_SCHEMA)
        .csv(resolve_path(relative_path))
    )


def extract_products(spark: SparkSession, relative_path: str) -> DataFrame:
    return (
        spark.read.option("header", True)
        .option("mode", "PERMISSIVE")
        .schema(PRODUCTS_SCHEMA)
        .csv(resolve_path(relative_path))
    )
