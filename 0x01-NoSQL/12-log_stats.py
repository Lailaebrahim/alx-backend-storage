#!/usr/bin/env python3
""" Python script that provides some stats about Nginx logs stored in MongoDB:"""
from pymongo import MongoClient


def print_logs_statistics(nginx_collection):
    '''Prints stats about Nginx request logs.
    '''
    print('{} logs'.format(nginx_collection.count_documents({})))
    print('Request Methods:')
    request_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in request_methods:
        req_count = len(list(nginx_collection.find({'method': method})))
        print('\tMethod {}: {}'.format(method, req_count))
    status_checks_count = len(list(
        nginx_collection.find({'method': 'GET', 'path': '/status'})
    ))
    print('{} status checks'.format(status_checks_count)


def analyze_logs():
    '''Provides some stats about Nginx logs stored in MongoDB.
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_logs_statistics(client.logs.nginx)


if __name__ == '__main__':
    analyze_logs()
