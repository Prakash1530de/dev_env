from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def clean_sales(sales: DataFrame, allow_zero_unit_price: bool = True):
    """Return (valid_sales, rejected_sales) with a rejection_reason column."""
    typed = (
        sales
        .withColumn("order_date", F.to_date("order_date", "yyyy-MM-dd"))
        .withColumn("quantity", F.col("quantity").cast("int"))
        .withColumn("unit_price", F.col("unit_price").cast("double"))
    )

    checks = [
        (F.col("sale_id").isNull() | (F.trim("sale_id") == ""), "missing_sale_id"),
        (F.col("customer_id").isNull() | (F.trim("customer_id") == ""), "missing_customer_id"),
        (F.col("product_id").isNull() | (F.trim("product_id") == ""), "missing_product_id"),
        (F.col("order_date").isNull(), "invalid_order_date"),
        (F.col("quantity").isNull(), "invalid_quantity"),
        (F.col("quantity") <= 0, "non_positive_quantity"),
        (F.col("unit_price").isNull(), "invalid_unit_price"),
        (F.col("unit_price") < 0, "negative_unit_price"),
    ]
    if not allow_zero_unit_price:
        checks.append((F.col("unit_price") == 0, "zero_unit_price"))

    reason = None
    for condition, label in checks:
        reason = F.when(condition, F.lit(label)) if reason is None else reason.when(condition, F.lit(label))

    classified = typed.withColumn("rejection_reason", reason.otherwise(F.lit(None).cast("string")))
    valid = classified.filter(F.col("rejection_reason").isNull()).drop("rejection_reason")
    rejected = classified.filter(F.col("rejection_reason").isNotNull())
    return valid, rejected


def enrich_sales(valid_sales: DataFrame, products: DataFrame) -> DataFrame:
    """Left join products so unmatched product IDs can be identified."""
    joined = valid_sales.join(products, on="product_id", how="left")
    return (
        joined
        .withColumn("line_total", F.round(F.col("quantity") * F.col("unit_price"), 2))
        .withColumn(
            "rejection_reason",
            F.when(F.col("product_name").isNull(), F.lit("unknown_product_id"))
        )
    )


def split_enriched(enriched: DataFrame):
    valid = enriched.filter(F.col("rejection_reason").isNull()).drop("rejection_reason")
    rejected = enriched.filter(F.col("rejection_reason").isNotNull())
    return valid, rejected
