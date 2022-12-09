# my-tontine

## This project is incomplete!

## How to run

- Create a virtual environment

    ```
    python -m venv env
    ```

    or

    ```
    virtualenv env
    ```

- Activate the virtual environment

  - On Windows :
    ```
    .\env\Scripts\activate
    ```

  - On linux or mac
    ```
    source ./env/bin/activate
    ```

- Install the requirements with

    ```
    pip install -r requirement.txt
    ```

- Migrate the databases

    ```
    python manage.py makemigrations
    ```

    ```
    python manage.py migrate
    ```

- Create superuser

    ```
    pythn manage.py createsuperuser
    ```

- Run the server

    ```
    python manage.py runserver
    ```
