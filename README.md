https://www.youtube.com/watch?v=K9AnJ9_ZAXE&list=PLwFJcsJ61oujAqYpMp1kdUBcPG0sE0QMT&index=1&t=2615s

course repo
https://github.com/coder2j/airflow-docker

python venv did not work because I have windows
====================================================
install docker desktop

check version
  docker --version
  docker-compose --version

To deploy Airflow on Docker Compose, you should fetch docker-compose.yaml. open wsl ubuntu in integrated terminal
  curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.1/docker-compose.yaml'
This downloads a docker-compose.yml file into your directory

In docker-compose.yml, change CeleryExecutor to LocalExecutor, 
then delete
      AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow
    AIRFLOW__CELERY__BROKER_URL: redis://:@redis:6379/0

also delete 
      redis:
      condition: service_healthy

and delete
    redis:
    image: redis:latest
    expose:
      - 6379
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 30s
      retries: 50
      start_period: 30s
    restart: always

and delete
    airflow-worker:
    <<: *airflow-common
    command: celery worker
    healthcheck:
      test:
        - "CMD-SHELL"
        - 'celery --app airflow.executors.celery_executor.app inspect ping -d "celery@$${HOSTNAME}"'
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    environment:
      <<: *airflow-common-env
      # Required to handle warm shutdown of the celery workers properly
      # See https://airflow.apache.org/docs/docker-stack/entrypoint.html#signal-propagation
      DUMB_INIT_SETSID: "0"
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

and delete
    # You can enable flower by adding "--profile flower" option e.g. docker-compose --profile flower up
  # or by explicitly targeted on the command line e.g. docker-compose up flower.
  # See: https://docs.docker.com/compose/profiles/
  flower:
    <<: *airflow-common
    command: celery flower
    profiles:
      - flower
    ports:
      - "5555:5555"
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:5555/"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

create more directories with
  mkdir -p ./dags ./logs ./plugins ./config

to initialize docker images
  docker compose up airflow-init

to start server in detached mode. This means they keep running in the background instead of stopping.
  docker-compose up -d

to check running containers
  docker ps

in browser, go to http://localhost:8080/ and enter "airflow" as username and password

add a .gitignore like this
  https://github.com/apache/airflow/blob/main/.gitignore

to shutdown containers
  docker-compose down -v
dash v means remove the volumes also
have to do this command in the same cli where you did docker-compose up -d

In docker-compose.yaml, change AIRFLOW__CORE__LOAD_EXAMPLES to false

Then do this again
  docker compose up airflow-init
then
  docker-compose up -d

Create our_first_dag.py like in tutorial repo

Have to reload the browser to see changes

================================================

How to manually backfill aka run tasks that were supposed to run in the past.

Check the containers with
  docker ps

Then open the container interactively, aka cli will stay in the container, with
  docker exec -it 0fea210a7334 bash

In the container, start the backfill with
  airflow dags backfill -s 2023-06-01 -e 2023-06-10 dag_with_catchup_backfill_v02

-s for start, -e for end date

To exit the container
  exit

======================================

crontab.guru helps in creating cron expressions

======================================

To see connections, like to postgres, go to admin/connections in the ui

Add port 5432 to docker-compose.yaml for postgres

To rebuild the postgres container
  docker-compose up -d --no-deps --build postgres

open dbeaver and use airflow as username and password in a new postgres connection

create a database named test

In airflow ui, in admin connections, add a connection with Connection Id = postgres_localhost
Connection type = Postgres
Schema = test
Username and password is = airflow
port = 5432
host = host.docker.internal // if it's not through docker, should be postgres, which comes from the service name in docker-compose.yaml, or localhost

The test database disappears when containers are stopped

===================================
2 ways of installing python dependencies

1 extending image
create a requirements.txt

create a Dockerfile

In command line
  docker build . --tag extending_airflow:latest
This builds an image using the Dockerfile in the current directory . and tag it with extending_airflow:latest

In docker-compose.yaml, change AIRFLOW_IMAGE_NAME:-apache/airflow:2.6.1 to
  AIRFLOW_IMAGE_NAME:-extending_airflow:latest

To check if dependencies are there, create dag_with_python_dependencies.py

Rebuild webserver and scheduler containers with
  docker-compose up -d --no-deps --build airflow-webserver airflow-scheduler
