# Stocks-Crypto ETL|Data Engineering Project

The goal of this project is to perform basic data analytics on a couple of stocks, ETFs and crypto I am currently hold using **docker** for conteinerization, **mage ai** for orchestration and data ingestion, **DuckDB** for storage and **Apache Superset** for visualisation

![Data Workflow](images/mageFinance.jpg)

## Data Sources
The Mage-AI Stocks Project uses data from Alpha Vantage. \
Access keys can be created by following the Alpha Vantage docs: https://www.alphavantage.co

## Pipeline
The data pipeline consists of the following steps:

1.  Connect to the Alpha Vantage API using the access keys
2.  Retrieve several finance data (Income statement, Cash flow etatement, Balance Sheet, Daily share prices) from the API
3.  Process the data using Mage-AI
4.  Save the processed data in Duck DB (aka Poor's man Data Warehouse)

A flowchart of the pipeline is shown below:

![Data Workflow](images/mageFinance.jpg) width=50% height=50%

This is how it looks in Mage

## Setup
To set up the project, follow these steps:

1.  Clone the repository and navigate to the project directory
2.  Build/Start the Docker container using Make mageBuild -> Make mageStart
3.  Run the pipeline -> This will save the results in duckDB
4.  Clone the Apache Superset repository
5.  To mount the duckDB file in Apache Superset navigate to the corresponding repo
and inside the ***docker-compose-non-dev.yml*** under ***x-superset-volumes: &superset-volumes*** copy the duckDB path in the **app** container
eg. - /{full path}/stockapp.duckdb:/app/stockapp.duckdb
6.  In Make file change the path of the Apache Superset ***docker-compose-non-dev.yml*** is located
7.  Fire up Apache superset by using Make supersetUP
8.  To succesfully run duckDB in Apache Superset do the following:
- Get the **super_app** container ID (you can docker ps to see the running containers)
- Then run docker exec -it **dockerId** sh -c "pip install duckdb_engine"

**!NOTE** probably I could have simplified the steps above by adding everything in docker-compose file :)

## Running the Pipeline
To run the pipeline, follow these steps:

1.  Access the Mage-AI web interface at http://localhost:6789/
2.  Click on the "wispy_wave" pipeline
3.  Click on "Run pipeline now" and "Run now"
4.  Enter the trigger and check the pipeline result
