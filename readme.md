# Python flask project

## A flask project with swagger api

### Packages used

- Flask==2.0.2
- flask-marshmallow==0.14.0
- Flask-SQLAlchemy==2.5.1
- flask-swagger-ui==3.36.0
- marshmallow==3.14.1
- marshmallow-sqlalchemy==0.27.0
- PyJWT==2.3.0
- requests==2.27.1
- SQLAlchemy==1.4.29
- urllib3==1.26.8
- Werkzeug==2.0.2

### Database Used

- PostgreSQL

### Installation

After cloning the project at first please install the above packages.

You can install these packages using:

- pip install -r requirements.txt

### For Database

In this project PostgreSQL is used.
After installing the packages please create a database. Provide your database name and password in the following line.

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:your_password@localhost:5432/database_name"

- You can do this by creating a database named 'Scrapydata1' and importing the newdata.sql file in newdata table in pgAdmin4.

* You also need to import users.sql file into your database the table name will be users

# Running the project

#### Atfirst please install and active your virtual environment:

- pip3 install virtualenv

Create a virtual environment

- virtualenv venv

Active your virtual environment

- source venv/bin/activate

After completing the database setup and installing the packages, you can run the project using the following command:

- python app.py

This will run the swagger ui in localhost: http://127.0.0.1:5000/

For searching and posting into the database at first you need to create a account.
Please Register here providing this information:
!["upper portion"](https://i.ibb.co/1JC6RsZ/register1.jpg)

Then Login with those credentials:
!["upper portion"](https://i.ibb.co/fphXk2M/login1.jpg)

After that you will get 45 seconds of access time to search or post data after that time you will be logged out and need to login again.
!["upper portion"](https://i.ibb.co/qgtDP8g/search1.jpg)
!["upper portion"](https://i.ibb.co/r4cD4Lk/search2.jpg)

You can post data into database:
!["upper portion"](https://i.ibb.co/gyp5nG2/addd.jpg)
