import smtplib
import uuid
import time
import os
import logging

from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor, as_completed

# SMTP CONFIGURATION
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "arnav2k20@gmail.com"
RECEIVER_EMAIL = "aka608693@gmail.com"

APP_PASSWORD = "bktv gvfz ihvp rfxt"

# TEST CONFIGURATION
TOTAL_EMAILS = 50
MAX_WORKERS = 10

SUBJECT = "SMTP Delivery Test"

BODY = """
Hello,

This is a harmless automated email
for testing my email filtering application.

No action is required.

Regards,
SMTP Testing Application
"""

# LOGGING
logging.basicConfig(
    filename="gmail_test.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def send_email(number):

    message_id = str(uuid.uuid4())

    message = MIMEText(
        BODY + f"\nTest ID: {message_id}"
    )

    message["Subject"] = SUBJECT
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    message["Message-ID"] = f"<{message_id}@gmail-test.local>"

    try:
        with smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT,
            timeout=30
        ) as server:

            server.ehlo()
            server.starttls()
            server.ehlo()

            server.login(
                SENDER_EMAIL,
                APP_PASSWORD
            )

            server.send_message(message)

        logging.info(f"Email {number} accepted by Gmail SMTP")

        return True, number

    except Exception as error:

        logging.error(f"Email {number} failed: {error}")

        return False, number


def main():

    if not APP_PASSWORD:
        print("GMAIL_APP_PASSWORD environment variable is missing.")
        return

    start = time.time()

    successful = 0
    failed = 0

    print("Starting Gmail SMTP test...")

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
    print(f"Time: {elapsed:.2f} seconds")

    print("Logs: gmail_test.log")


if __name__ == "__main__":
    main()