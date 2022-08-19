# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


import json
import os

import boto3

import db2

from base import BaseInterface


SECRET_ARN = os.environ["DB2_CONFIGURATION_ARN"]


def get_db2_configuration():
    """Sets DB2 Configuration from Secrets Manager

    :return: Response string from secrets manager
    :rtype: str
    """
    sm = boto3.client("secretsmanager")
    print("getting secret")
    print(SECRET_ARN)
    response = sm.get_secret_value(SecretId=SECRET_ARN)
    print(response)
    return json.loads(response["SecretString"])


def set_db2_connection():
    """Initiates connection to AS/400"""
    global schema, connection
    print("getting config")
    configuration = get_db2_configuration()
    print(configuration)
    schema = configuration["schema"]
    connection = db2.connect(**configuration)


def handler(event, context):
    """Lambda handler

    :param event: Event from trigger source
    :type event: dict
    """
    print("starting now")
    set_db2_connection()
    params = ("key_attribute_1", "key_attribute_2")
    interface = BaseInterface(connection, schema)
    print(interface._example_select_query(*params))
    print(interface._example_delete_query(*params))
    db2.disconnect(connection)
