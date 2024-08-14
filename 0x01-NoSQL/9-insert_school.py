#!/usr/bin/env python3
""" a Python function that inserts a new document in a collection based on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a MongoDB collection based on kwargs.
    
    :param mongo_collection: pymongo collection object
    :param kwargs: keyword arguments representing the document to insert
    :return: the new _id of the inserted document
    """
    # Insert the document using the kwargs
    result = mongo_collection.insert_one(kwargs)

    # Return the _id of the newly inserted document
    return result.inserted_id
