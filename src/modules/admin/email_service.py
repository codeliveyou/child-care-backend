import smtplib
from email.mime.text import MIMEText
from constants import Constants  # Assuming you have email credentials stored in a constants file

def send_email(sender_email: str, recipient_email: str, subject: str, body: str):
    try:
        # Create MIMEText object for the email body
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = Constants.SMTP_USERNAME
        msg['To'] = recipient_email

        # Connect to the SMTP server
        with smtplib.SMTP(Constants.SMTP_SERVER, Constants.SMTP_PORT) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(Constants.SMTP_USERNAME, Constants.SMTP_PASSWORD)  # Login to the email account
            server.sendmail(sender_email, recipient_email, msg.as_string())  # Send the email

        print(f"Email sent successfully to {recipient_email}")

    except Exception as e:
        print(f"Error sending email: {e}")
        raise
