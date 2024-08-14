#!/usr/bin/env python3
"""Python function that returns the list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
        """
    Returns the list of schools having a specific topic.

    :param mongo_collection: pymongo collection object
    :param topic: string, the topic to search for
    :return: list of schools (documents) that have the specified topic
    """
    schools = list(mongo_collection.find({"topics": topic}))
    return schools
