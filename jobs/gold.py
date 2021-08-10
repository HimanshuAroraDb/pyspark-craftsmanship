from dependencies.spark import start_spark
from config.config import settings
from pyspark.sql.functions import *


def main():
    # start Spark application and get Spark session, logger
    spark, log = start_spark(app_name='covid_gold_job')

    # log that main ETL job is starting
    log.warn('covid_bronze_job is up-and-running')

    # execute ETL pipeline
    log.info(f'Reading raw file: {settings.sliver_delta_path}')
    data = extract_data(spark)

    transformed_data = transform(data)

    log.info(f'Writing gold table at: {settings.gold_delta_path}')
    load_data(transformed_data, settings.gold_delta_path)

    # log the success and terminate Spark application
    log.warn('covid_gold_job is finished')
    return None


def extract_data(spark):
    df = (
        spark
            .read
            .format("delta")
            .load(settings.sliver_delta_path))

    return df


def transform(dataframe):
    transformed_df = (
        dataframe
            .groupBy("date", "state")
            .agg(
            sum("positive").alias("total_positive"),
            sum("negative").alias("total_negative"),
            sum("recovered").alias("total_recovered"),
            sum("death").alias("total_death"),
            sum("hospitalizedCurrently").alias("total_hospitalized_currently"),
            sum("onVentilatorCurrently").alias("total_on_ventilator_currently")
        ).orderBy("date")
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
