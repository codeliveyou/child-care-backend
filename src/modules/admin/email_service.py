import smtplib
from email.mime.text import MIMEText
from constants import Constants  # Assuming you have email credentials stored in a constants file

# def send_email(recipient_email: str, subject: str, body: str):
#     try:
#         # Create MIMEText object for the email body
#         msg = MIMEText(body)
#         msg['Subject'] = subject
#         msg['From'] = Constants.SMTP_USERNAME
#         msg['To'] = recipient_email

#         # Connect to the SMTP server
#         with smtplib.SMTP(Constants.SMTP_SERVER, Constants.SMTP_PORT) as server:
#             server.starttls()  # Upgrade the connection to secure
#             server.login(Constants.SMTP_USERNAME, Constants.SMTP_PASSWORD)  # Login to the email account
#             server.sendmail('codetankstn@gmail.com', recipient_email, msg.as_string())  # Send the email

#         print(f"Email sent successfully to {recipient_email}")

#     except Exception as e:
#         print(f"Error sending email: {e}")
#         raise



def send_email(recipient_email: str, subject: str, body: str):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = Constants.SMTP_USERNAME
        msg['To'] = recipient_email

        print(f"Connecting to SMTP server {Constants.SMTP_SERVER} on port {Constants.SMTP_PORT}...")
        with smtplib.SMTP(Constants.SMTP_SERVER, Constants.SMTP_PORT, timeout=30) as server:
            server.starttls()
            print("Starting TLS encryption...")
            server.login(Constants.SMTP_USERNAME, Constants.SMTP_PASSWORD)
            print(f"Logged in as {Constants.SMTP_USERNAME}")
            server.sendmail(Constants.SMTP_USERNAME, recipient_email, msg.as_string())
            print(f"Email sent successfully to {recipient_email}")

    except smtplib.SMTPException as smtp_error:
        print(f"SMTP error occurred: {smtp_error}")
        raise
    except Exception as e:
        print(f"Error sending email: {e}")
        raise
