from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'coder2j',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='dag_with_catchup_backfill_v02',
    default_args=default_args,
    start_date=datetime(2023, 6, 1),
    schedule_interval='@daily', # equivalent to 0 0 * * * chron
    catchup=False # defaults to True. If False, it won't run tasks that were supposed to run in the past aka it won't backfill. Could manually backfill by going into the container, read README.md.
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo This is a simple bash command!'
    )