from os import environ

GITHUB_TOKEN = environ.get("GITHUB_TOKEN")
VAULT_ADDRESS = environ.get("VAULT_ADDRESS")
GATEWAY_ADDRESS = environ.get("GATEWAY_ADDRESS")
RUN_ENV = environ.get("RUN_ENV")
SERVICE_NAME = environ.get("SERVICE_NAME")
API_VER = environ.get("API_VER", "v1")

CREATE_NEW_APPLICANT = GATEWAY_ADDRESS + "/applicant"
ONE_APPLICANT = GATEWAY_ADDRESS + "/applicant/{0}"
GET_APPLICANT_AUTH = GATEWAY_ADDRESS + "/applicant/{0}/authorization"
ONE_ADMIN = GATEWAY_ADDRESS + "/admin/{0}"
GET_ADMIN_AUTH = GATEWAY_ADDRESS + "/admin/{0}/authorization"
