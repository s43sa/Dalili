from flask import Flask
from flask_mysqldb import MySQL 


app = Flask(__name__)
# secret key to sign session 
app.secret_key = '4289876543234567890'


#database connection details below
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Dalili'

# Intialize MySQL
mysql = MySQL(app)