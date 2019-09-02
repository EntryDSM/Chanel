import re

from sanic import Sanic
from sanic.log import logger
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from python_http_client.exceptions import BadRequestsError, UnauthorizedError

from chanel.common.client.vault import settings


def send_email(to_email: str, title: str, content: str):
    message = Mail(
        from_email="entrydsm@dsm.hs.kr",
        to_emails=to_email,
        subject=title,
        html_content=content
    )

    try:
        client = SendGridAPIClient(settings.sendgrid_api_key)
        response = client.send(message)

        return response.status_code

    except BadRequestsError:
        logger.error("failed to send email: Bad request")

    except UnauthorizedError:
        logger.error("failed to send email: Unauthorized")


def email_checker(email: str) -> bool:
    expression = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    result: bool = expression.match(email) is not None

    return result
