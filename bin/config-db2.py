#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


import getpass
import json

import boto3

import common


print("Configure DB2 connection details:")
common.set_cwd()
sm = boto3.client("secretsmanager")
secret_id = common.get_db2_configuration()
response = sm.get_secret_value(SecretId=secret_id)
configuration = json.loads(response["SecretString"])


def get_value(key):
    old_value = configuration[key]
    if key != "password":
        prompt = f"{key.capitalize()} [{old_value}]: "
        print(type(prompt))
        new_value = input(prompt)
    else:
        mask = "********" if old_value else ""
        prompt = f"{key.capitalize()} [{mask}]: "
        new_value = getpass.getpass(prompt)
    return new_value if new_value else old_value


for key in ("hostname", "database", "schema", "username", "password"):
    configuration[key] = get_value(key)

secret_string = json.dumps(configuration)
response = sm.put_secret_value(SecretId=secret_id, SecretString=secret_string)
if response and response.get("ARN") == secret_id:
    print("New values configured")
else:
    print("Configuration NOT changed")
