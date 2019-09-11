import re
from functools import wraps

from python_http_client.exceptions import BadRequestsError, UnauthorizedError
from sanic.request import Request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from chanel.common.client.vault import settings
from chanel.common.exception import InvalidSyntaxException, BadRequest, Unauthorized


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
        raise BadRequest("failed to send email.")

    except UnauthorizedError:
        raise Unauthorized("failed to send email.")


def check_email_syntax(email_url_index: int = False):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            email = request.json.get("email") if not email_url_index else request.url.split("/")[email_url_index]

            if not email:
                raise BadRequest("Email doesn't exist")

            expression = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
            if not expression.match(email):
                raise BadRequest("Email with invalid form.")

            response = await f(*args, **kwargs)

            return response

        return decorated_function

    return decorator
