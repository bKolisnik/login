Flask starter template

to activate venv

. venv/bin/activate

to install reqs

pip install -r requirements.txt

to use test server

python3 app.py

to use production server

gunicorn --bind 0.0.0.0:5000 app:app

to create a new db, create a db in sql
to create table do 

from config import Config
from app import db, create_app
db.create_all(app=create_app(Config))

in the terminal ^^^^