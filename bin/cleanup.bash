#!/usr/bin/env bash

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


set -e

cd "$(dirname "${BASH_SOURCE[0]}")/.."

environment_file="${1-.env}"
source "bin/${environment_file}"

bin/cleanup.py
