https://www.youtube.com/watch?v=K9AnJ9_ZAXE&list=PLwFJcsJ61oujAqYpMp1kdUBcPG0sE0QMT&index=1&t=2615s

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

