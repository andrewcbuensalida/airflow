from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor


default_args = {"owner": "coder2j", "retries": 5, "retry_delay": timedelta(minutes=10)}


with DAG(
    dag_id="dag_with_minio_s3_v02",
    start_date=datetime(2023, 6, 1),
    schedule_interval="@daily",
    default_args=default_args,
) as dag:
    task1 = S3KeySensor(
        task_id="sensor_minio_s3",
        bucket_name="airflow",  # should be the same in minio and aws
        bucket_key="data.csv",  # this watches for changes of the file in s3
        aws_conn_id="minio_s3_conn",
        mode="poke",
        poke_interval=5,
        timeout=30,
    )
