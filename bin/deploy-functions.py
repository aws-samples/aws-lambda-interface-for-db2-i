#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


import os

import common


common.set_cwd()

template_filename = ".aws-sam/build/functions_cfn.yml"
template = open(template_filename).read()
image_repository = common.get_image_repository()
secret_arn = common.get_db2_configuration()
stack_name = (
    os.environ["PROJECT_NAME"]
    + "-"
    + os.environ["ENVIRONMENT_NAME"]
    + "-functions"
)
parameters = {
    "Project": os.environ["PROJECT_NAME"],
    "Environment": os.environ["ENVIRONMENT_NAME"],
    "DB2ConfigurationArn": secret_arn,
    "DB2VpcId": os.environ["VPC_ID"],
    "DB2SubnetIds": os.environ["SUBNET_IDS"],
    "DB2InjectorBaseImage": f"{image_repository}:pyodbc-db2",
}

capabilities = ["CAPABILITY_IAM"]
common.deploy_stack(stack_name, template, parameters, capabilities)
