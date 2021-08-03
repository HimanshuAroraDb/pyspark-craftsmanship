"""
spark.py
~~~~~~~~

Module containing helper function for use with Apache Spark
"""

from pyspark.sql import SparkSession
from dependencies import logging


def start_spark(app_name='my_spark_app', master='local[*]'):
    # get Spark session factory
    spark_builder = (
        SparkSession
        .builder
        .master(master)
        .appName(app_name))

    # create session and retrieve Spark logger object
    spark_sess = spark_builder.getOrCreate()
    spark_logger = logging.Log4j(spark_sess)

    return spark_sess, spark_logger
