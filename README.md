# leitner_box
Telegram bot which provides Leitner courses


## Postgres
Change values in brackets to what you set in .env file for db name, user and password.
```commandline
sudo -u postgres psql
postgres=# CREATE DATABASE [your db name];
postgres=# CREATE USER [your db user] WITH PASSWORD [your db password];
postgres=# GRANT ALL PRIVILEGES ON DATABASE [your db name] TO [your db user];
postgres=# \q
```

## Migrate Database
```angular2html
 python main migrate
```
### After each change in models do the following steps 
```angular2html
alembic stamp head
alembic revision -m "[Change a filed of leitner]"
alembic upgrade head
python main migrate
```

## Run the project
```angular2html
python main run
```
