from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.template.loader import render_to_string
from .tokens import email_verification_token
from django.core.mail import EmailMessage

def send_verification_email(request, user):
    """ Send email verification to user """

    current_site = get_current_site(request)
    subject = "Activate Your Account"

    token = email_verification_token.make_token(user)

    #encode user id
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    #generate activation link
    # example output - http://example.com/activate/MQ/token123/
    activation_link = f"http://{current_site.domain}{reverse('users:activate', kwargs={'uidb64' : uid, 'token' : token})}"

    print("Activation link", activation_link)
    # message = render_to_string("emails/email_verification_html", {
    #     "user": user,
    #     "activation_link": activation_link,
    # })

    # email = EmailMessage(subject, message, to=[user.email])
    # email.send()
