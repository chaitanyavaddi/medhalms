import logging
import threading
import resend
from django.conf import settings

logger = logging.getLogger(__name__)


def _get_client():
    resend.api_key = getattr(settings, 'RESEND_API_KEY', '')
    return resend


def send_email(to, subject, html, from_email=None):
    client = _get_client()
    if not resend.api_key:
        logger.warning('RESEND_API_KEY not set, skipping email to %s', to)
        return
    try:
        client.Emails.send({
            'from': from_email or settings.EMAIL_FROM_NOREPLY,
            'to': [to] if isinstance(to, str) else to,
            'subject': subject,
            'html': html,
        })
    except Exception as e:
        logger.error('Failed to send email to %s: %s', to, e)


def send_batch(emails):
    client = _get_client()
    if not resend.api_key or not emails:
        return
    try:
        for i in range(0, len(emails), 100):
            client.Batch.send(emails[i:i + 100])
    except Exception as e:
        logger.error('Failed to send batch emails: %s', e)


def send_email_async(to, subject, html, from_email=None):
    threading.Thread(
        target=send_email,
        args=(to, subject, html, from_email),
        daemon=True,
    ).start()


def send_batch_async(emails):
    threading.Thread(
        target=send_batch,
        args=(emails,),
        daemon=True,
    ).start()
