# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


import logging
import threading
import yaml

import forwarder.api
import forwarder.cfg.file
import forwarder.worker

config_filename = "/tmp/forwarder.yaml"

host_config = {
    "source": {
        "addr": "127.0.0.1",
        "port": 8471,
    },
    "destination": {
        "addr": "to-be-provided",
        "port": 9471,
        "use-ssl-tls": True,
        "ssl-tls": {
            "verify": True,
            "check-host": True,
            "required": "required",
            "ca-bundle": "/etc/ssl/certs/ca-bundle.crt",
        },
    },
}


def start(db2_hostname):
    host_config["destination"]["addr"] = db2_hostname
    forwarder_config = {"version": 2, "hosts": [host_config]}
    with open(config_filename, "w") as config_file:
        yaml.dump(forwarder_config, config_file)
    forwarder.api.logger = logging.getLogger()
    forwarder.api.logger.setLevel(logging.WARNING)
    forwarder.api.config = forwarder.cfg.file.ConfigFile()
    forwarder.api.config.load(config_filename)
    forwarder.api.verbose = True
    threading.Thread(target=forwarder.worker.worker).start()
