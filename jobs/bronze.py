

from dependencies.spark import start_spark


def main():
    # start Spark application and get Spark session, logger
    spark, log = start_spark(app_name='covid_bronze_job')

    # log that main ETL job is starting
    log.warn('covid_bronze_job is up-and-running')

    # execute ETL pipeline
    data = extract_data(spark)
    load_data(data, "./out/covid/bronze")

    # log the success and terminate Spark application
    log.warn('covid_bronze_job is finished')
    return None


def extract_data(spark):
    df = (
        spark
        .read
        .option("header", True)
        .csv('tests/test_data/covid.csv'))

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