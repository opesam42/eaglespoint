import requests
from django.conf import settings
import os
from dotenv import load_dotenv
import json
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.template import engines

load_dotenv()

MJML_API_URL = "https://api.mjml.io/v1/render"

def compile_mjml(mjml_content):
    """Sends MJML content to the MJML API and returns the compiled HTML."""
    
    auth = (settings.MJML_APP_ID, settings.MJML_SECRET_KEY)

    payload = {
        "mjml":mjml_content,
    }

    try:
        response = requests.post(MJML_API_URL, json=payload, auth=auth)
        response.raise_for_status()

        return response.json().get('html')

    except requests.exceptions.RequestException as e:
        # Handle request exceptions (network errors, etc.)
        print(f"Error calling MJML API: {e}")
        return None

def load_mjml_from_file(template_file):

    """ Load MJML content from file """
    full_path = os.path.join(settings.BASE_DIR, 'emails', 'templates', 'emails', template_file)
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            mjml_content = f.read()
        return mjml_content
    except Exception as e:
        print(f"Error loading MJML file: {e}")
        return None


class EmailSender:
    def __init__(self, recipient_email, subject, template_path, template_context=None):
        self.recipient_email = recipient_email
        self.subject = subject
        self.template_path = template_path
        self.template_context = template_context or {}

    def send(self):
        try:
            # subject = "Welcome to SkedlEase"
            mjml_template_content = load_mjml_from_file(self.template_path)

            # pass template_context 
            django_engines = engines['django']
            compiled_template = django_engines.from_string(mjml_template_content)
            rendered_mjml_template = compiled_template.render(self.template_context)

            final_html_content = compile_mjml(rendered_mjml_template)

            email = EmailMessage(
                subject=self.subject,
                body=final_html_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[self.recipient_email],
            )
            email.content_subtype = "html"
            email.encoding = 'utf-8'
            email.send()
            print('email sent')
            return True
        
        except Exception as error:
            print(f"Error sending email: {error}")
            return False