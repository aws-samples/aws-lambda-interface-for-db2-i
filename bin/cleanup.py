#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


import os

import boto3

import common


common.set_cwd()

# delete images from ECR repository
ecr_repo_name = (
    os.environ["PROJECT_NAME"]
    + "-"
    + os.environ["ENVIRONMENT_NAME"]
    + "-db2-injector"
)
ecr = boto3.client("ecr")
response = ecr.describe_images(repositoryName=ecr_repo_name)
image_list = [key["imageDigest"] for key in response["imageDetails"]]
imageIds = []
for image in image_list:
    imageIds.append({"imageDigest": image})

if imageIds:
    ecr.batch_delete_image(repositoryName=ecr_repo_name, imageIds=imageIds)

# delete base stack
base_stack_name = (
    os.environ["PROJECT_NAME"] + "-" + os.environ["ENVIRONMENT_NAME"] + "-base"
)
common.delete_stack(base_stack_name)

# delete function stack
function_stack_name = (
    os.environ["PROJECT_NAME"]
    + "-"
    + os.environ["ENVIRONMENT_NAME"]
    + "-functions"
)
common.delete_stack(function_stack_name)
