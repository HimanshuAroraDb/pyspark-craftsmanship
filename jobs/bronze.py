

from dependencies.spark import start_spark
from config.config import settings

def main():
    # start Spark application and get Spark session, logger
    spark, log = start_spark(app_name='covid_bronze_job')

    # log that main ETL job is starting
    log.warn('covid_bronze_job is up-and-running')

    # execute ETL pipeline
    log.info(f'Reading raw file: {settings.input_path}')
    data = extract_data(spark)
    log.info(f'Writing bronze table at: {settings.bronze_delta_path}')
    load_data(data, settings.bronze_delta_path)

    # log the success and terminate Spark application
    log.warn('covid_bronze_job is finished')
    return None


def extract_data(spark):
    df = (
        spark
        .read
        .option("header", True)
        .csv(settings.input_path))

    return df


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