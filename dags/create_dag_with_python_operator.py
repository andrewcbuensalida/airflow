from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'coder2j',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


def greet(some_dict, ti):
    print("some dict: ", some_dict)
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')
    print(f"Hello World! My name is {first_name} {last_name}, "
          f"and I am {age} years old!")


def get_name(ti):
    ti.xcom_push(key='first_name', value='Jerry') # this is how to pass information from one task to another. By default, every function's return value will be pushed to Admin/xcoms, max size is 48kb.
    ti.xcom_push(key='last_name', value='Fridman')


def get_age(ti):
    ti.xcom_push(key='age', value=19)


with DAG(
    default_args=default_args,
    dag_id='our_dag_with_python_operator_v07',
    description='Our first dag using python operator',
    start_date=datetime(2023, 6, 1),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={'some_dict': {'a': 1, 'b': 2}}
    )

    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )

    task3 = PythonOperator(
        task_id='get_age',
        python_callable=get_age
    )

    [task2, task3] >> task1 # task 1 is task 2 and 3s downstream