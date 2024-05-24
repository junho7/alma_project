import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from config import settings

def send_confirmation_email(lead_data):

    try:
        message = MIMEMultipart()
        message["From"] = settings.SENDER_EMAIL
        message["To"] = ", ".join([lead_data["email"], settings.ATTORNEY_EMAIL])
        message["Subject"] = "Lead Submission Confirmation"
        body = (
            f"Dear {lead_data['first_name']},\n\nThank you for submitting your form.\n\n"
            f"First name: {lead_data['first_name']}\n"
            f"Last name: {lead_data['last_name']}\n"
            f"email: {lead_data['email']}\n"
            f"Resume/CV: {lead_data['resume_filename']} is attached\n\n"
            f"Sincerely,\nThe Alma Team"
        )
        message.attach(MIMEText(body, "plain"))

        if "resume_contents" in lead_data:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(lead_data["resume_contents"])
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {lead_data['resume_filename']}",
            )
            message.attach(part)

        with smtplib.SMTP_SSL('smtp.mail.yahoo.com', port=465) as server:
            server.login(settings.SMTP_USERNAME, settings.SMTP_APP_PASSWORD)
            server.send_message(message)

    except Exception as e:
        print(f"Error sending email: {e}")
