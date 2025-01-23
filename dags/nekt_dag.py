from datetime import datetime

import requests
from airflow.decorators import dag, task
from airflow.sensors.base import BaseSensorOperator

API_URL = "https://api.nekt.ai/api/v1"
API_TOKEN = ""
PIPELINE_SLUG = ""


class NektPipelineSensor(BaseSensorOperator):
    def __init__(self, pipeline_slug, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pipeline_slug = pipeline_slug

    def poke(self, context):
        headers = {"X-API-Token": API_TOKEN}
        url = f"{API_URL}/pipelines/{self.pipeline_slug}/"
        response = requests.get(url, headers=headers)

        response.raise_for_status()
        data = response.json()
        run_status = data.get("current_status")
        print(f"Run status: {run_status}")

        if run_status in ["queued", "running"]:
            return False
        if run_status == "success":
            return True
        if run_status == "failed":
            raise Exception("Pipeline failed")


default_args = {
    "owner": "airflow",
}


@dag(
    dag_id="nekt_dag",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
)
def nekt_dag():
    @task
    def trigger_pipeline(pipeline_slug: str, full_sync: bool = False):
        headers = {"X-API-Token": API_TOKEN}
        url = f"{API_URL}/pipelines/{pipeline_slug}/trigger/"
        data = {"full_sync": full_sync}
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()

    wait_for_pipeline = NektPipelineSensor(
        task_id="wait_for_pipeline",
        pipeline_slug=PIPELINE_SLUG,
        poke_interval=10,
    )

    @task
    def do_something_when_pipeline_ends():
        print("Do something")

    trigger_pipeline(PIPELINE_SLUG) >> wait_for_pipeline >> do_something_when_pipeline_ends()


dag_instance = nekt_dag()
