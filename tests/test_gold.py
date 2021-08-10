import os
from jobs import gold
from chispa import assert_df_equality


def test_covid_gold_transformation(spark_session):
    test_dir_path = os.path.dirname(os.path.realpath(__file__))

    input_df = (
        spark_session
            .read
            .option("header", True)
            .csv(f'{test_dir_path}/test_data/covid_gold_test.csv'))

    expected_df = (
        spark_session
            .read
            .parquet(f'{test_dir_path}/test_data/expected/covid_gold'))

    gold_df = gold.transform(input_df)

    assert_df_equality(gold_df, expected_df)
