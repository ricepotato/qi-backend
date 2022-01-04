import os
import ssl
import pymongo
import configparser


def get_mongo_client(host, user, password):
    """  mongodb+srv://ricepotato:<password>@cluster0-gpvm5.gcp.mongodb.net/wetube?retryWrit """
    connection_string = f"mongodb+srv://{user}:{password}@{host}"
    client = pymongo.MongoClient(
        connection_string, ssl=True, tlsAllowInvalidCertificates=True
    )
    return client


def get_client():
    host = os.environ.get("MONGODB_HOST")
    user = os.environ.get("MONGODB_USER")
    password = os.environ.get("MONGODB_PASSWORD")
    client = get_mongo_client(host, user, password)
    return client
