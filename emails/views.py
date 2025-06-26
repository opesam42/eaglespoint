from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

from .mjml import EmailSender
from .tokens import email_verification_token

# Create your views here.
def send_account_verification_email(request, user, context={}):
    """ Send email verification to user """

    current_site = get_current_site(request)
    subject = "Activate Your Account"

    token = email_verification_token.make_token(user)

    #encode user id
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    #generate activation link
    # example output - http://example.com/activate/MQ/token123/
    activation_link = f"http://{current_site.domain}{reverse('user:activate', kwargs={'uidb64' : uid, 'token' : token})}"

    print("Activation link", activation_link)

    return EmailSender(
        recipient_email=user.email,
        subject="Verify Your Eaglespoint Account",
        template_path='account-verification.html',
        template_context={
            'user': user,
            'activation_link': activation_link,
        },
    ).send()
