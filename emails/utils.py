from mjml import EmailSender

def send_patient_welcome_email(to_email, context={}):
    return EmailSender(
        to_email=to_email,
        email_subject="Reset Password",
        template_path='user/reset-password.mjml',
        context=context,
    ).send()