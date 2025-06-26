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

def compile_mjml(mjml_content, output_file_path):
    """Sends MJML content to the MJML API and returns the compiled HTML, and optionally writes it to a file."""
    print(settings.MJML_APP_ID)
    auth = (settings.MJML_APP_ID, settings.MJML_SECRET_KEY)

    payload = {
        "mjml":mjml_content,
    }

    try:
        response = requests.post(MJML_API_URL, json=payload, auth=auth)
        response.raise_for_status()
        html_output = response.json().get('html')

        if output_file_path:
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(html_output)

        return html_output

    except requests.exceptions.RequestException as e:
        # Handle request exceptions (network errors, etc.)
        print(f"Error calling MJML API: {e}")
        return None

def load_mjml_from_file(file_path):

    """ Load MJML content from file """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            mjml_content = f.read()
        return mjml_content
    except Exception as e:
        print(f"Error loading MJML file: {e}")
        return None
