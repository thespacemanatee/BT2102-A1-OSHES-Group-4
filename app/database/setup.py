from pymongo import MongoClient
import mysql.connector

MONGODB_URL = 'mongodb://localhost:27017'

mongo_client = MongoClient(MONGODB_URL)
db = mongo_client.OSHES
Products = db.Products
Items = db.Items

mysql_client = mysql.connector.connect(
    host="localhost",
    user='root',
    password='password'
)

mycursor = mysql_client.cursor()

mycursor.execute("SHOW DATABASES")

for x in mycursor:
    print(x)