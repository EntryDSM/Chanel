from datetime import timedelta
from os import environ

GITHUB_TOKEN = environ.get("GITHUB_TOKEN")
VAULT_ADDRESS = environ.get("VAULT_ADDRESS")
RUN_ENV = environ.get("RUN_ENV")
SERVICE_NAME = environ.get("SERVICE_NAME")
API_VER = environ.get("API_VER", "v1")

APPLICANT = "Applicant"
HERMES = "http://hermes/api/v1"
CREATE_NEW_APPLICANT = HERMES + "/applicant"
ONE_APPLICANT = HERMES + "/applicant/{0}"
GET_APPLICANT_AUTH = HERMES + "/applicant/{0}/authorization"
ONE_ADMIN = HERMES + "/admin/{0}"
GET_ADMIN_AUTH = HERMES + "/admin/{0}/authorization"

VERIFY_EMAIL_TITLE = "[대덕소프트웨어마이스터고등학교] 입학전형시스템 회원가입 인증코드"
VERIFY_EMAIL_CONTENT = "대덕소프트웨어마이스터고등학교 입학전형시스템에 가입하기 위해 다음 코드를 입력해주세요. %s"
