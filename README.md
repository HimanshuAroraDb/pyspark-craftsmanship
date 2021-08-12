![build status](https://github.com/HimanshuAroraDb/pyspark-craftsmanship/actions/workflows/cicd.yml/badge.svg)

# Pyspark Craftsmanship

This project provides a standard model for pyspark projects enforcing python, software cratsmanship and CI/CD best practices.
It relies on [poetry](https://python-poetry.org/) a python packaging and dependency management library. We have used [dynaconf](https://www.dynaconf.com/) for multi environment configuration management and [pytest](https://docs.pytest.org/en/6.2.x/) & [chispa](https://github.com/MrPowers/chispa) for pyspark unit testing.

You can use this model as an accelerator to bootstrap your own pyspark project and take advantage of all the best practices.

### Project structure

![Structure](https://github.com/HimanshuAroraDb/pyspark-craftsmanship/blob/main/structure.png?raw=true)

In this model we are using covid-19 Kaggle dataset. In the jobs package you will find 3 jobs which represent bronze, silver and gold layers of multihop data pipeline. These jobs are quite simple and straightfoward as it's just a model to help you bootstrap but in real life you can have a lot more jobs in there with various level of complexity depending on the usecase. 

The dependencies package is supposed to have all the utility modules that are supposed to be used by multiple jobs. In this model we have two modules. First one is spark.py which creates the spark session and another one is logger.py which initizes the logger for pyspark.

Dynaconf is used for project configuration management. The config file (settings.toml) is present in config package where you can add environment (dev/qa/prod for example) specific configurations. Dynaconf also allows to override the configurations at run time using environment variables.


### CI/CD

We have used the GitHub [actions](https://docs.github.com/en/actions) for CI/CD part. As you can see in the [cicd workflow file](https://github.com/HimanshuAroraDb/pyspark-craftsmanship/blob/main/.github/workflows/cicd.yml). As the part of CICD workflow we start by installing all the necesary dependencies like python, jdk and other python packages defined in the poerty description file. We also install and set up [databricks-cli](https://docs.databricks.com/dev-tools/cli/index.html) as it is needed to interact with workspace's dbfs. 
Once all is installed and setup we run the unit tests, prepare poetry wheel package and copy that package to databricks [dbfs](https://docs.databricks.com/data/databricks-file-system.html) file system.

We have used Databricks as the deployment destination but you are not bound to do that. By chaning the deployment step (i.e. *Deploy artifact* in [cicd.yml](https://github.com/HimanshuAroraDb/pyspark-craftsmanship/blob/main/.github/workflows/cicd.yml)) of CICD workflow you can deploy the wheel package to a data platform/cloud/repository of your choice. And if you prefer to publish your project's wheel package as a library to PyPi or to a private repositiry then run `poerty publish` command.

### Commands

To install dependencies: `poetry install`

To run unit tests: `poetry run pytest tests -v --junitxml="result.xml"`

To build a wheel package: `poetry build`

To run pyspark jobs locally: `poetry run spark-submit --packages io.delta:delta-core_2.12:1.0.0 --py-files dist/jobs-0.1.0-py3-none-any.whl jobs/bronze.py`

To run all the job as pipeline on Databricks execute following steps:
 - Import `data_pipeline_notebook.py` file as notebook on Databricks.
 - Make sure to change the input & output path configurations in settings.toml file according to your cloud settings.
 - Once the configurations are set accordingly then run the CI/CD pipeline so that the recent wheel can be deplyed to dbfs.
 - As you set input/output paths also make sure your cluster have necessary permission to access those paths (either via passthrough or mounting via service principal, access key etc.).
 - Install project's wheel package available on dbfs as a library on your cluster.
 - Don't forget to set `ENV_FOR_DYNACONF=production` env variable in your cluster conf to actiave production configuration settings.
 - Now you can execute your notebook.
 - So either run your notebook interactively or schedule it as a cron job taking in account the above steps.
