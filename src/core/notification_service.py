import smtplib
from email.mime.text import MIMEText
from src.config_manager import config_manager
from src.utils.logger import setup_logger

logger = setup_logger('notification_service', 'logs/notifications.log')

class NotificationService:
    def __init__(self):
        self.email_sender = config_manager.get("EMAIL_SENDER")
        self.email_password = config_manager.get("EMAIL_PASSWORD")
        self.email_receiver = config_manager.get("EMAIL_RECEIVER")

    def send_email(self, subject, body):
        if not all([self.email_sender, self.email_password, self.email_receiver]):
            logger.warning("Email credentials missing.")
            return False

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.email_sender
        msg['To'] = self.email_receiver

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.email_sender, self.email_password)
                server.send_message(msg)
            logger.info(f"Email sent: {subject}")
            return True
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False

    def notify(self, opportunity):
        message = f"""
NEW {opportunity.category.upper()} OPPORTUNITY

Title: {opportunity.title}
Company: {opportunity.company}
Score: {opportunity.relevance_score}/100

Summary:
{opportunity.summary}

Apply Here:
{opportunity.link}
"""
        self.send_email(f"Career Alert: {opportunity.title} @ {opportunity.company}", message)

notification_service = NotificationService()
