from pymongo import AsyncMongoClient

# Connecting to mongodb image from docker-compose
mongo_client: AsyncMongoClient = AsyncMongoClient(
    "mongodb://admin:admin@mongo:27017"
)