# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


ARG BASE_IMAGE

FROM $BASE_IMAGE

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt \
 && rm requirements.txt

COPY src/ ./
