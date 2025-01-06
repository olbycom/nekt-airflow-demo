# nekt-airflow-demo

Instructions to how a standalone instance of airflow and trigger a Nekt pipeline in a DAG.

# Prerequisites

You need to have Docker installed and running.

Download it at [Get Docker](https://docs.docker.com/get-started/get-docker/).

# Setup

Clone this repo:

```bash
git clone git@github.com:olbycom/nekt-airflow-demo.git
```

Make the setup script executable:

```bash
chmod +x setup.sh
```

The setup script will create the necessary folder structure, download the most updated airflow docker compose file and setup the airflow containers.

Run the setup:

```bash
./setup.sh
```

# Running Airflow

To start airflow using docker, run:

```bash
docker compose up
```

**Airflow will be available at http://localhost:8080/**

To stop the containers, run:

```bash
docker compose down
```

# Nekt DAG

You can access the Nekt DAG example at [http://localhost:8080/dags/nekt_dag](http://localhost:8080/dags/nekt_dag)

It is composed by two main tasks:

- trigger_pipeline: A Python task that will trigger a DAG at Nekt;
- wait_for_pipeline: A sensor that will track if the pipeline execution succeeded or failed.

You need to update the API Token (contact Nekt support to request a token) and Pipeline slug at `nekt_dag.py`:

```python-repl
API_TOKEN = ""
PIPELINE_SLUG = ""
```
