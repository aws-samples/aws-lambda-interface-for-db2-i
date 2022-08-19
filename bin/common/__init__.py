# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


import __main__
import base64
import json
import os
import subprocess
import yaml

import boto3
import botocore
import samtranslator.public.translator
import samtranslator.translator.transform
import samtranslator.yaml_helper


PROJECT_NAME = os.environ["PROJECT_NAME"]
ENVIRONMENT_NAME = os.environ["ENVIRONMENT_NAME"]


def set_cwd():
    script_folder = os.path.abspath(os.path.dirname(__main__.__file__))
    os.chdir(f"{script_folder}/..")


def yaml_to_json(input_filename, output_filename):
    with open(input_filename) as input_file, open(output_filename, "w") as output_file:
        template = samtranslator.yaml_helper.yaml_parse(input_file.read())
        json.dump(template, output_file, indent=2)
    print(f"Converted {input_filename} to {output_filename}")


def get_stack_for_environment(stack_name):
    cfn = boto3.client("cloudformation")
    response = cfn.describe_stacks(StackName=stack_name)
    for stack in response["Stacks"]:
        parameters = {
            p["ParameterKey"]: p["ParameterValue"] for p in stack["Parameters"]
        }
        environment_name = parameters.get("Environment")
        if environment_name == ENVIRONMENT_NAME:
            return stack


def get_image_repository():
    ecr = boto3.client("ecr")
    response = ecr.describe_repositories()
    repositories = response["repositories"]
    for repository in repositories:
        if (  # TODO: need improvements, this just checks for environment and project name
            ENVIRONMENT_NAME in repository["repositoryName"]
            and PROJECT_NAME in repository["repositoryName"]
        ):
            return repository["repositoryUri"]


def login_to_repository(image_repository):
    ecr = boto3.client("ecr")
    registry_id = image_repository.split(".")[0]
    response = ecr.get_authorization_token(registryIds=[registry_id])
    token = base64.b64decode(
        response["authorizationData"][0]["authorizationToken"]
    ).decode()
    username, password = token.split(":")
    command = (
        "docker",
        "login",
        "--username",
        username,
        "--password-stdin",
        image_repository,
    )
    subprocess.run(command, input=password.encode())


def get_db2_configuration():
    cfn = boto3.client("cloudformation")
    stack_name = PROJECT_NAME + "-" + ENVIRONMENT_NAME + "-base"
    response = cfn.describe_stacks(StackName=stack_name)
    stack = response["Stacks"][0]
    outputs = {
        output["OutputKey"]: output["OutputValue"] for output in stack["Outputs"]
    }
    return outputs.get("DB2ConfigurationArn")


def deploy_stack(name, template, parameters={}, capabilities=[]):
    print(f"Deploying stack {name}")
    cfn = boto3.client("cloudformation")
    current_stacks = cfn.describe_stacks()
    stack_exists = name in (s["StackName"] for s in current_stacks["Stacks"])
    deploy_stack_func = cfn.update_stack if stack_exists else cfn.create_stack
    stack_wait_condition = (
        "stack_update_complete" if stack_exists else "stack_create_complete"
    )
    parameters = [
        {"ParameterKey": k, "ParameterValue": v} for k, v in parameters.items()
    ]
    try:
        deploy_stack_func(
            StackName=name,
            TemplateBody=template,
            Parameters=parameters,
            Capabilities=capabilities,
        )
        cfn.get_waiter(stack_wait_condition).wait(StackName=name)
        print("Stack deployed successfully")
    except botocore.exceptions.ClientError as error:
        if "No updates are to be performed" in str(error):
            print("Stack up-to-date")
        else:
            raise
    try:
        response = cfn.describe_stacks(StackName=name)
        return response["Stacks"][0]["Outputs"][0]["OutputValue"]  # TODO: change
    except KeyError as error:
        if "Outputs" not in str(error):
            raise


def package_functions(template_filename):
    class ManagedPolicyStub:
        def load(self):
            return {"": ""}

    image_repository = get_image_repository()
    login_to_repository(image_repository)
    parameter_overrides = f"ParameterKey=DB2InjectorBaseImage,ParameterValue={image_repository}:pyodbc-db2"
    build_command = (
        "sam",
        "build",
        "--use-container",
        "--cached",
        "--parallel",
        "--template",
        template_filename,
        "--parameter-overrides",
        parameter_overrides,
    )
    package_command = (
        "sam",
        "package",
        "--template",
        ".aws-sam/build/template.yaml",
        "--image-repository",
        image_repository,
    )
    subprocess.run(build_command)
    result = subprocess.run(package_command, capture_output=True, encoding="utf-8")
    sam_template = samtranslator.yaml_helper.yaml_parse(result.stdout)
    cfn_template = samtranslator.translator.transform.transform(
        sam_template, {}, ManagedPolicyStub()
    )
    return yaml.dump(cfn_template)


def delete_stack(name):
    print(f"Deleting stack {name}")
    cfn = boto3.client("cloudformation")
    current_stacks = cfn.describe_stacks()
    stack_exists = name in (s["StackName"] for s in current_stacks["Stacks"])
    if stack_exists:
        cfn.delete_stack(StackName=name)
        cfn.get_waiter("stack_delete_complete").wait(StackName=name)
    else:
        print(f"Stack '{name}' does not exist.")
