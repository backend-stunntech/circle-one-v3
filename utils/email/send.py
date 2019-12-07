from importlib import import_module

import boto3
from django.conf import settings
from django.template.loader import get_template


def send_email(recipient: str,
               subject: str,
               body_text: str,
               body_html: str,
               sender=f"{settings.DEFAULT_SENDER_EMAIL}@{settings.MASTER_DOMAIN}"):
    # credentials are set via environment, which is automatically picked by boto3
    client = boto3.Session().client(service_name='ses', region_name='us-east-1', api_version='2010-12-01')
    charset = 'UTF-8'
    # Provide the contents of the email.
    return client.send_email(
        Destination={
            'ToAddresses': [
                recipient,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': charset,
                    'Data': body_html,
                },
                'Text': {
                    'Charset': charset,
                    'Data': body_text,
                },
            },
            'Subject': {
                'Charset': charset,
                'Data': subject,
            },
        },
        Source=sender,
    )


def render_and_send_mail(template_path: str, context=None, **kwargs):
    """
        Send an html/plaintext email using aws ses.
    """
    initial_context = dict()
    email_context_processors = getattr(settings, 'EMAIL_CONTEXT_PROCESSORS', [])
    plaintext_template_name, html_template_name, subject_template_name = map(
        lambda file_name: f"email-templates/{template_path}/{file_name}", [
            'body.txt', 'body.html', 'subject.txt'
        ])
    for processor in email_context_processors:
        module_name, processor_func_name = processor.rsplit('.', maxsplit=1)
        processor_function = getattr(import_module(module_name), processor_func_name)
        initial_context.update(processor_function())
    initial_context.update(context)
    text_email = get_template(plaintext_template_name).render(initial_context)
    html_email = get_template(html_template_name).render(initial_context)
    subject = get_template(subject_template_name).render(initial_context)
    return send_email(body_text=text_email, body_html=html_email, subject=subject, **kwargs)
