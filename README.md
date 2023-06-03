https://www.youtube.com/watch?v=K9AnJ9_ZAXE&list=PLwFJcsJ61oujAqYpMp1kdUBcPG0sE0QMT&index=1&t=2615s

====================================================

python3 --version gives an error
Python was not found; run without arguments to install from the Microsoft Store, or disable this shortcut from Settings > Manage App Execution Aliases.
but python --version works


====================================================

first create the python environment with 
  python -m venv py_env
this creates the folder py_env

got an error when doing in powershell
  source py_env/bin/activate
so activate it using bash terminal
  source py_env/Scripts/activate

to leave venv
  deactivate

install apacha airflow here
  https://github.com/apache/airflow#installing-from-pypi

  pip install 'apache-airflow==2.6.1' \
 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.6.1/constraints-3.8.txt"

 