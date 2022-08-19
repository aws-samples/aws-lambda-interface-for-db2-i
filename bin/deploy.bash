#!/usr/bin/env bash

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


set -e

cd "$(dirname "${BASH_SOURCE[0]}")/.."

environment_file="${1-.env}"
source "bin/${environment_file}"

bin/deploy-base.py

echo
bin/config-db2.py
echo

images/pyodbc-db2/bin/build.bash
images/pyodbc-db2/bin/push.bash

bin/build-functions.py
bin/deploy-functions.py
