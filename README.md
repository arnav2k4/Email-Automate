Steps:

1. "dig MX <domain>" - Helps find the mail server
2. "nc -vz <mail_smtp_domain> 587 (eg: smtp.gmail.com)" - Checks if 587 port is open or not
3. Find the "App Password", "Sender's Mail" and "Reciever's Mail".
4. Set the no. of mails to be sent and the number of worker nodes.
5. Execute the spamMail.py using "python spamMail.py"

To add phishing links, malwares, etc., change the body of the mail and add the malware or phishing links in the body.
