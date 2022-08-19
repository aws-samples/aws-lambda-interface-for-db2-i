#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


import common


common.set_cwd()

template_filename = "functions/functions_cfn.yml"
template = common.package_functions(template_filename)
translated_template_filename = ".aws-sam/build/functions_cfn.yml"
with open(translated_template_filename, "w") as template_file:
    template_file.write(template)
