# pyspark-craftsmanship

To install dependencies: `poetry install`

To run unit tests: `poetry run pytest`

To build a wheel package: `poetry build`

To run pyspark jobs locally: `poetry run spark-submit --packages io.delta:delta-core_2.12:1.0.0 --py-files dist/jobs-0.1.0-py3-none-any.whl jobs/bronze.py`
