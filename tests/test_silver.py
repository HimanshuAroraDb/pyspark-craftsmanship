
import os
from jobs import silver


def test_covid_sliver_transformation(spark_session):
    test_dir_path = os.path.dirname(os.path.realpath(__file__))

    input_df = (
        spark_session
            .read
            .option("header", True)
            .csv(f'{test_dir_path}/test_data/covid_silver_test.csv'))

    sliver_df = silver.transform(input_df)

    assert sliver_df.count() == 4
