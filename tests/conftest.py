
import pytest
from dependencies.spark import start_spark

@pytest.fixture(scope='session')
def spark_session():
    spark_session, _ = start_spark(app_name='unit_test')
    yield spark_session