#!/usr/bin/env python3
"""Python function that returns the list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """
    Changes all topics of a school document based on the name.

    :param mongo_collection: pymongo collection object
    :param name: string, the school name to update
    :param topics: list of strings, the list of topics approached in the school
    """
    result = mongo_collection.find({"topics": topics})

    return result

