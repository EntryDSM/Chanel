import re

from sanic import Sanic
from sanic.log import logger
from sendgrid import SendGridAPIClient, ApiKeyIncludedException
from sendgrid.helpers.mail import Mail
from python_http_client.exceptions import BadRequestsError, UnauthorizedError


def send_email(to_email: str, title: str, content: str, app: Sanic):
    message = Mail(
        from_email="entrydsm@dsm.hs.kr",
        to_emails=to_email,
        subject=title,
        html_content=content
    )

    try:
        client = SendGridAPIClient(app.config["SENDGRID_API_KEY"])
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
