#!/usr/bin/env bash

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


set -e

cd "$(dirname "${BASH_SOURCE[0]}")/.."

image_name="${PROJECT_NAME}-${ENVIRONMENT_NAME}-db2-injector:pyodbc-db2"

docker build -t "${image_name}" .
