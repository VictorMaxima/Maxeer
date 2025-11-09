import requests
from django.conf import settings
import resend
resend.api_key = settings.RESEND_API_KEY

def send_resend_email(to_email, subject, text_body, html_body=None):
    """
    Send an email using Resend API
    """
    r = resend.Emails.send({
  "from": "onboarding@resend.dev",
  "to": to_email,
  "subject": subject,
  "html": html_body
})
