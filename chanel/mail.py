from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from chanel.setting import SENDGRID_API_KEY


def send_email(to_email: str, title: str, content: str):
    message = Mail(
        from_email="entrydsm@dsm.hs.kr",
        to_emails=to_email,
        subject=title,
        html_content=content
    )

    try:
        client = SendGridAPIClient(SENDGRID_API_KEY)
        response = client.send(message)
        return response.status_code
    except Exception as e:
        print(str(e))
