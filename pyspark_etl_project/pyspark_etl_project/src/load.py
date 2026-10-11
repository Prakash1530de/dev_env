from pyspark.sql import DataFrame
from .utils import resolve_path


def write_parquet(df: DataFrame, relative_path: str, mode: str = "overwrite") -> None:
    output_path = resolve_path(relative_path)
    df.write.mode(mode).parquet(output_path)


def write_csv(df: DataFrame, relative_path: str, mode: str = "overwrite") -> None:
    output_path = resolve_path(relative_path)
    df.write.mode(mode).option("header", True).csv(output_path)
