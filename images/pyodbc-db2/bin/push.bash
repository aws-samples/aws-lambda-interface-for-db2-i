#!/usr/bin/env bash

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


set -e

cd "$(dirname "${BASH_SOURCE[0]}")/.."

account_id="$(aws sts get-caller-identity --query 'Account' --output text)"
region="us-east-1"
repository_name="${account_id}.dkr.ecr.${region}.amazonaws.com"

image_name="${PROJECT_NAME}-${ENVIRONMENT_NAME}-db2-injector:pyodbc-db2"
image_tag="${repository_name}/${image_name}"

aws ecr get-login-password --region "${region}" | docker login --username AWS --password-stdin "${repository_name}"

docker tag "${image_name}" "${image_tag}"
docker push "${image_tag}"
