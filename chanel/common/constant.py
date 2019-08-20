from os import environ

GITHUB_TOKEN = environ.get("GITHUB_TOKEN")
VAULT_ADDRESS = environ.get("VAULT_ADDRESS")
RUN_ENV = environ.get("RUN_ENV")
SERVICE_NAME = environ.get("SERVICE_NAME")
API_VER = environ.get("API_VER", "v1")
