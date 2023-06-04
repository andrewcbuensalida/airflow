# This is the shorter syntax version of create_dag_with_python_operator.py
from datetime import datetime, timedelta

from airflow.decorators import dag, task


default_args = {
    'owner': 'coder2j',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

@dag(dag_id='dag_with_taskflow_api_v03', 
     default_args=default_args, 
     start_date=datetime(2023, 6, 1), 
     schedule_interval='@daily')
def hello_world_etl():

    @task(multiple_outputs=True) # True if returning a dictionary
    def get_name(): # Whatever the function returns will be put in Admin/xcoms. This will put first_name, last_name, AND the dict in xcom.
        return {
            'first_name': 'aaaa',
            'last_name': 'bbbb'
        }

    @task()
    def get_age():
        return 19

    @task()
    def greet(first_name, last_name, age):
        print(f"Hello World! My name is {first_name} {last_name} "
              f"and I am {age} years old!")
    
    name_dict = get_name()
    age = get_age()
    greet(first_name=name_dict['first_name'], 
          last_name=name_dict['last_name'],
          age=age)

greet_dag = hello_world_etl()
