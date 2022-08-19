#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


import os

import common


common.set_cwd()

template_filename = "infrastructure/base_cfn.yml"
template = open(template_filename).read()

stack_name = (
    os.environ["PROJECT_NAME"] + "-" + os.environ["ENVIRONMENT_NAME"] + "-base"
)

parameters = {
    "Project": os.environ["PROJECT_NAME"],
    "Environment": os.environ["ENVIRONMENT_NAME"],
}

common.deploy_stack(stack_name, template, parameters)
