import os
import ssl
import smtplib
import uuid
import time
import logging

from concurrent.futures import ThreadPoolExecutor, as_completed
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP CONFIGURATION
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "Sender's Email"
RECEIVER_EMAIL = "Receiver's Email"

APP_PASSWORD = "app_password"

# TEST CONFIGURATION
TOTAL_EMAILS = 5
MAX_WORKERS = 1

SUBJECT = "SMTP Delivery Test"
TEST_URL = "https://youtube.com"

# LOGGING
logging.basicConfig(
    filename="gmail_test.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def create_email(number):

    message_id = str(uuid.uuid4())

    message = MIMEMultipart("alternative")

    message["Subject"] = f"{SUBJECT} #{number}"
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    message["Message-ID"] = f"<{message_id}@gmail-test.local>"

    plain_body = f"""
Hello,

This is a harmless automated email
for testing my email filtering application.

Test destination:
RESET PASSWORD

No action is required.

Test Number: {number}
Test ID: {message_id}

Regards,
SMTP Testing Application
"""

    html_body = f"""
<html>
<body style="font-family: Arial, sans-serif;">

    <h3>SMTP Testing</h3>

    <p>This is automated test email #{number}.</p>

    <p>Test ID: {message_id}</p>

    <a href="{TEST_URL}"
       style="
           display: inline-block;
           padding: 12px 25px;
           background-color: #2563eb;
           color: white;
           text-decoration: none;
           border-radius: 6px;
           font-size: 16px;
           font-weight: bold;
       ">
       RESET PASSWORD
    </a>

    <p>Test destination: {TEST_URL}</p>

    <p>No action is required.</p>

    <p>Regards,<br>
    SMTP Testing Application</p>

</body>
</html>
"""

    message.attach(MIMEText(plain_body, "plain"))
    message.attach(MIMEText(html_body, "html"))

    return message


def send_email(number):

    try:
        message = create_email(number)

        context = ssl.create_default_context()

        with smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT,
            timeout=30
        ) as server:

            server.ehlo()
            server.starttls(context=context)
            server.ehlo()

            server.login(
                SENDER_EMAIL,
                APP_PASSWORD
            )

            server.send_message(message)

        logging.info("Email %s accepted by Gmail SMTP", number)

        return True, number

    except Exception as error:

        logging.error(
            "Email %s failed: %s",
            number,
            error
        )

        return False, number


def main():

    if not APP_PASSWORD:
        print("GMAIL_APP_PASSWORD environment variable is missing.")
        return

    start = time.time()

    successful = 0
    failed = 0

    print(f"Starting {TOTAL_EMAILS} test emails...")
    print(f"Concurrent workers: {MAX_WORKERS}\n")

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        futures = [
            executor.submit(send_email, i)
            for i in range(1, TOTAL_EMAILS + 1)
        ]

        for future in as_completed(futures):

            success, number = future.result()

            if success:
                successful += 1
                print(f"[SUCCESS] Email {number}")

            else:
                failed += 1
                print(f"[FAILED] Email {number}")

    elapsed = time.time() - start

    print("\n========== RESULTS ==========")
    print(f"Total: {TOTAL_EMAILS}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Workers: {MAX_WORKERS}")
    print(f"Time: {elapsed:.2f} seconds")
    print("Logs: gmail_test.log")


if __name__ == "__main__":
    main()
