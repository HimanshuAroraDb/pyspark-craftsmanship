![build status](https://github.com/HimanshuAroraDb/pyspark-craftsmanship/actions/workflows/cicd.yml/badge.svg)

# pyspark-craftsmanship

This project provides a standard model for pyspark projects enforcing the most cutting edge python, software cratsmanship and CI/CD best practices.
It relies on [poetry](https://python-poetry.org/) a python packaging and dependency management library. We have used [dynaconf](https://www.dynaconf.com/) for project configuration management and [pytest](https://docs.pytest.org/en/6.2.x/) & [chispa](https://github.com/MrPowers/chispa) for pyspark unit testing.

To install dependencies: `poetry install`

To run unit tests: `poetry run pytest tests`

To build a wheel package: `poetry build`

To run pyspark jobs locally: `poetry run spark-submit --packages io.delta:delta-core_2.12:1.0.0 --py-files dist/jobs-0.1.0-py3-none-any.whl jobs/bronze.py`

To run all the job as pipeline on Databricks execute following steps:
 - Import `data_pipeline_notebook.py` file as notebook on Databricks
 - Make sure to change the input & output path configurations in settings.toml file according to your cloud settings
 - As you set input/output paths also make sure your cluster have necessary permission to access those paths (either via passthrough or mounting via service principal, access key etc.)
 - Install this project's build package as a wheel library on your cluster
 - Don't forget to set `ENV_FOR_DYNACONF=production` env variable un your cluster conf to actiave production conf
 - Now you can execute your notebook
 - So either run your notebook interactively or schedule it as a cron job taking in account the above steps
