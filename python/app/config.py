import logging
import os
from dataclasses import dataclass

LOCAL_CONFIG = {
    "bootstrap.servers": "20.73.225.80:9094",
    "security.protocol": "ssl",
    "ssl.ca.location": "./ca.crt",
}

CLUSTER_CONFIG = {
    "bootstrap.servers": "my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092"
}


@dataclass
class Config:
    @classmethod
    def get(self):
        if "ENVIRONMENT" not in os.environ:
            raise ValueError("The environment variable ENVIRONMENT is not set!")
        environment = os.environ.get("ENVIRONMENT")
        if environment == "local":
            logging.info("Loaded configuration for environment `local`.")
            return LOCAL_CONFIG
        if environment == "cluster":
            logging.info("Loaded configuration for environment `cluster`.")
            return CLUSTER_CONFIG
        raise ValueError(
            f"ENVIRONMENT should be 'local' or 'cluster', but found {environment}"
        )
