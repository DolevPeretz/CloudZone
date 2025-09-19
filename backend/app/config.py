import os

TABLE_NAME = os.getenv("TABLE_NAME", "customer_ids")
AWS_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "eu-central-1"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


EVENT_BUS_NAME    = os.getenv("EVENT_BUS_NAME", "default")
EVENT_SOURCE      = os.getenv("EVENT_SOURCE", "customers.api")
EVENT_DETAIL_TYPE = os.getenv("EVENT_DETAIL_TYPE", "Customer.Submitted")