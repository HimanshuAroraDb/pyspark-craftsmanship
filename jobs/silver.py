from dependencies.spark import start_spark
from config.config import settings
from pyspark.sql.functions import *


def main():
    # start Spark application and get Spark session, logger
    spark, log = start_spark(app_name='covid_sliver_job')

    # log that main ETL job is starting
    log.warn('covid_bronze_job is up-and-running')

    # execute ETL pipeline
    log.info(f'Reading raw file: {settings.bronze_delta_path}')
    data = extract_data(spark)
    log.info(f'Writing sliver table at: {settings.sliver_delta_path}')
    load_data(data, settings.sliver_delta_path)

    # log the success and terminate Spark application
    log.warn('covid_sliver_job is finished')
    return None


def extract_data(spark):
    df = (
        spark
            .read
            .format("delta")
            .load(settings.bronze_delta_path))

    return df


def transform(dataframe):
    transformed_df = (
        dataframe
            .filter(
            col("hospitalizedCurrently").isNotNull() &
            col("positive").isNotNull() &
            col("negative").isNotNull() &
            col("onVentilatorCurrently").isNotNull() &
            col("recovered").isNotNull() &
            col("death").isNotNull() &
            col("date").isNotNull() &
            col("state").isNotNull()
        )
    )
    return transformed_df


def load_data(df, output_path):
    (df
     .write
     .mode("overwrite")
     .format("delta")
     .save(output_path))
    return None


# entry point for this job
if __name__ == '__main__':
    main()
