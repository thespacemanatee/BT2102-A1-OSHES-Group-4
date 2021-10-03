from pymongo import MongoClient

MONGODB_URL = 'mongodb://localhost:27017'

client = MongoClient(MONGODB_URL)
db = client.OSHES
Products = db.Products
Items = db.Items
