import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings

def send_confirmation_email(lead_data):

    try:
        message = MIMEMultipart()
        message["From"] = settings.ADMIN_EMAIL_ADDRESS
        message["To"] = ", ".join([lead_data.email, settings.ATTORNEY_EMAIL_ADDRESS])
        message["Subject"] = "Lead Submission Confirmation"
        body = (
            f"Dear {lead_data.first_name},\n\nThank you for submitting your form.\n\n"
            f"First name: {lead_data.first_name}\n"
            f"Last name: {lead_data.last_name}\n"
            f"email: {lead_data.email}\n"
            f"Resume/CV: {lead_data.resume}\n\n"
            f"Sincerely,\nThe Alma Team"
        )
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(
            settings.SMTP_URL, settings.SMTP_PORT
        ) as server:
            server.send_message(message)

    except Exception as e:
        print(f"Error sending email: {e}")