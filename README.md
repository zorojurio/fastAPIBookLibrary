## Requirements
Python 3.9

## Set Env Variables
create a .env file locally
go to .env.example and follow the same format


## Usage
To run the server, please execute the following from the root directory:

```
python -m venv venv
pip install -r requirements.txt

python3 main.py
```

Your Swagger definition lives here:

```
http://localhost:8000/docs
```




To run Alembic migrations and perform migrations

```
alembic revision --message="migration_name" --autogenerate

alembic upgrade head
```