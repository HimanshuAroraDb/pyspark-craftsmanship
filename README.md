![build status](https://github.com/HimanshuAroraDb/pyspark-craftsmanship/actions/workflows/cicd.yml/badge.svg)

# Pyspark Craftsmanship

This project provides a standard model for pyspark projects enforcing the most cutting edge python, software cratsmanship and CI/CD best practices.
It relies on [poetry](https://python-poetry.org/) a python packaging and dependency management library. We have used [dynaconf](https://www.dynaconf.com/) for multi environment configuration management and [pytest](https://docs.pytest.org/en/6.2.x/) & [chispa](https://github.com/MrPowers/chispa) for pyspark unit testing.

You can use this model as an accelerator to bootstrap your own pyspark project and take advantage of all the best practices.

### Project structure

![Structure](https://github.com/HimanshuAroraDb/pyspark-craftsmanship/blob/main/structure.png?raw=true)

### CI/CD

We have used the GitHub [actions](https://docs.github.com/en/actions) for CI/CD part. As you can see in the [cicd workflow file](https://github.com/HimanshuAroraDb/pyspark-craftsmanship/blob/main/.github/workflows/cicd.yml). As the part of CICD workflow we start by installing all the necesary dependencies like python, jdk and other python packages defined in the poerty description file. We also install and set up [databricks-cli](https://docs.databricks.com/dev-tools/cli/index.html) as it is needed to interact with workspace's dbfs. 
Once all is installed and setup we run the unit tests, prepare poetry wheel package and copy that package to databricks [dbfs](https://docs.databricks.com/data/databricks-file-system.html) file system.

### Necessary commands

To install dependencies: `poetry install`

To run unit tests: `poetry run pytest tests`

To build a wheel package: `poetry build`

To run pyspark jobs locally: `poetry run spark-submit --packages io.delta:delta-core_2.12:1.0.0 --py-files dist/jobs-0.1.0-py3-none-any.whl jobs/bronze.py`

To run all the job as pipeline on Databricks execute following steps:
 - Import `data_pipeline_notebook.py` file as notebook on Databricks.
 - Make sure to change the input & output path configurations in settings.toml file according to your cloud settings.
 - Once the configurations are set accordingly then run the CI/CD pipeline so that the recent wheel can be deplyed to dbfs.
 - As you set input/output paths also make sure your cluster have necessary permission to access those paths (either via passthrough or mounting via service principal, access key etc.).
 - Install project's wheel package available on dbfs as a library on your cluster.
 - Don't forget to set `ENV_FOR_DYNACONF=production` env variable un your cluster conf to actiave production conf.
 - Now you can execute your notebook.
 - So either run your notebook interactively or schedule it as a cron job taking in account the above steps.
