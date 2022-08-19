# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


import pyodbc

import db2.forward


def connect(hostname, database, schema, username, password, tls):
    connection_params = {
        "DRIVER": "IBM i Access ODBC Driver",
        "SYSTEM": hostname,
        "DATABASE": database,
        "UID": username,
        "PWD": password,
    }
    if tls:
        connection_params["SYSTEM"] = "127.0.0.1"
    connection_string = ";".join(
        f"{k}={v}" for k, v in connection_params.items()
    )
    try:
        return pyodbc.connect(connection_string)
    except Exception:
        db2.forward.start(hostname)
        return pyodbc.connect(connection_string)


def disconnect(connection):
    cursor = connection.cursor()
    cursor.close()
    connection.close()
