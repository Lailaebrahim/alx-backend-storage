#!/usr/bin/env python3
""" Python function that lists all documents in a collection"""


def list_all(mongo_collection):
    """
    Lists all documents in a MongoDB collection.
    
    :param mongo_collection: pymongo collection object
    :return: list of all documents, or empty list if no documents
    """
    # Fetch all documents from the collection
    documents = list(mongo_collection.find())

    # Return the list of documents (will be empty if no documents found)
    return documents
