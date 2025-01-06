curl -O https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml && \
mkdir -p ./logs ./plugins && \
echo "AIRFLOW_UID=$(id -u)" > .env && \
echo "AIRFLOW_GID=0" >> .env && \
docker compose up airflow-init