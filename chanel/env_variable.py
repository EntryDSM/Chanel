from os import environ

VAULT_ADDRESS = environ.get("VAULT_ADDRESS")
VAULT_TOKEN = environ.get("VAULT_TOKEN", None)
RUN_ENV = environ.get("RUN_ENV")
GITHUB_TOKEN = environ.get("GITHUB_TOKEN", None)
SERVICE_NAME = environ.get("SERVICE_NAME", "chanel")
