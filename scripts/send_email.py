import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


SENDER = os.environ["GMAIL_SENDER"]
PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
RECIPIENT = os.environ["GMAIL_RECIPIENT"]


def main():

    with open(
        "marketing_morning.html",
        "r",
        encoding="utf-8"
    ) as file:
        html = file.read()

    today = datetime.now().strftime("%d/%m/%Y")

    message = MIMEMultipart("alternative")

    message["Subject"] = (
        f"☀️ Marketing Morning — {today}"
    )

    message["From"] = SENDER
    message["To"] = RECIPIENT

    message.attach(
        MIMEText(
            html,
            "html",
            "utf-8"
        )
    )

    print("Connexion à Gmail...")

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            SENDER,
            PASSWORD
        )

        server.sendmail(
            SENDER,
            RECIPIENT,
            message.as_string()
        )

    print(
        f"Email envoyé à {RECIPIENT}"
    )


if __name__ == "__main__":
    main()
