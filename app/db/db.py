# Connection to mongodb
from .client import mongo_client

# Database name mydb
database = mongo_client["mydb"]