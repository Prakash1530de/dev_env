from pyspark.sql import SparkSession
from .extract import extract_sales, extract_products
from .transform import clean_sales, enrich_sales, split_enriched
from .load import write_parquet, write_csv
from .utils import load_config


def main():
    config = load_config()
    spark_cfg = config["spark"]
    spark = (
        SparkSession.builder
        .appName(spark_cfg["app_name"])
        .master(spark_cfg["master"])
        .config("spark.sql.shuffle.partitions", spark_cfg["shuffle_partitions"])
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    try:
        sales = extract_sales(spark, config["paths"]["sales_input"])
        products = extract_products(spark, config["paths"]["products_input"])

        valid_sales, invalid_sales = clean_sales(
            sales,
            allow_zero_unit_price=config["quality"]["allow_zero_unit_price"],
        )
        enriched = enrich_sales(valid_sales, products)
        curated, unmatched_products = split_enriched(enriched)

        rejected = invalid_sales.unionByName(unmatched_products, allowMissingColumns=True)

        print("Input sales:", sales.count())
        print("Curated sales:", curated.count())
        print("Rejected sales:", rejected.count())

        write_parquet(curated, config["paths"]["curated_output"])
        write_csv(rejected, config["paths"]["rejected_output"])
        print("ETL pipeline completed.")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
