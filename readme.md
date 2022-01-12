source env/bin/activate
flask db init
flask db migrate
flask db upgrade