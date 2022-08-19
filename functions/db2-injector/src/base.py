# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


import functools


_table_names = {
    "table_name_1": "EXAMPLE1",
    "table_name_2": "EXAMPLE2",
}

_query_methods = [
    {
        "name": "_example_select_query",
        "base": "_execute_transaction",
        "table": "table_name_1",
        "query": """
        SELECT FROM {0}.{1} WHERE ATTRIBUTE_1 = ? AND ATTRIBUTE_2 = ?
        """,
    },
    {
        "name": "_example_delete_query",
        "base": "_execute_transaction",
        "table": "table_name_2",
        "query": """
        DELETE FROM {0}.{1} WHERE ATTRIBUTE_1 = ? AND ATTRIBUTE_2 = ?
        """,
    },
]


class BaseInterface:
    """Allows transformations and operations between DDB and AS400 data."""

    def _execute_transaction(self, query, *params):
        """Executes a given SQL query

        :param query: query expression
        :type query: str
        """
        self._cursor.execute(query, *params)
        self._cursor.commit()

    def _append_methods(self, table_names, query_methods):
        """Creates methods based on queries and tables in each class

        :param table_names: names of AS/400 tables used by class
        :type table_names: dict
        :param query_methods: query expressions used by class
        :type query_methods: dict
        """
        self._table_names = getattr(self, "_table_names", {})
        self._table_names.update(table_names)
        self._query_methods = getattr(self, "_query_methods", [])
        self._query_methods.extend(query_methods)

    def _construct_methods(self, schema):
        """Constructs methods for AS/400 queries using schema

        :param schema: AS/400 schema to use
        :type schema: str
        """
        for method in self._query_methods:
            method_name = method["name"]
            base_method = getattr(self, method["base"])
            table_name = self._table_names[method["table"]]
            query = method["query"].format(schema, table_name)
            setattr(self, method_name, functools.partial(base_method, query))

    def __init__(self, connection, schema):
        """Initializes base class

        :param connection: AS/400 connection details
        :type connection: PyODBC connection object
        :param schema: AS/400 schema details
        :type schema: str
        """
        self._append_methods(_table_names, _query_methods)
        self._construct_methods(schema)
        self._cursor = connection.cursor()
