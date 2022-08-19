# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


import json
import os

import db2


db_configuration = json.loads(os.environ["DB2_CONFIGURATION"])

db2_connection = db2.connect(**db_configuration)


def handler(event, context):
    query = event["query"]
    print(f"Running query: {query}")
    cursor = db2_connection.cursor()
    rows = cursor.execute(query)
    for row in rows.fetchall():
        print(row)
