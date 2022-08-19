# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


FROM public.ecr.aws/lambda/python:3.8 as base

COPY lib/*.rpm /tmp/

RUN yum update -y \
 && yum install -y \
      gcc-c++ \
      unixODBC-devel \
 && pip install --no-cache-dir -t /opt/python/lib/python3.8/site-packages \
      forwarder==0.12.35 \
      hexdump==3.3 \
      pyodbc==4.0.30 \
 && rpm -i /tmp/*.rpm

FROM public.ecr.aws/lambda/python:3.8

RUN yum update -y \
 && yum install -y \
      unixODBC \
 && yum clean all

COPY --from=base /etc/odbcinst.ini /etc/
COPY --from=base /opt/ibm/iaccess/conv_tables/ /opt/ibm/iaccess/conv_tables/
COPY --from=base /opt/ibm/iaccess/lib64/ /opt/ibm/iaccess/lib64/
COPY --from=base /usr/lib64/libcwbcore.so /usr/lib64/

COPY --from=base /opt/python/lib/python3.8/site-packages/ /opt/python/lib/python3.8/site-packages/

COPY --from=base /var/task/ ./

COPY src/ ./

CMD [ "main.handler" ]
