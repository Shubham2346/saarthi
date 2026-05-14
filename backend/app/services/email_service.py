"""Send transactional email via SMTP (blocking calls run in a thread pool)."""

import asyncio
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from app.config import get_settings

logger = logging.getLogger(__name__)


def _send_sync(to_addr: str, subject: str, html_body: str, text_body: str) -> None:
    settings = get_settings()
    if not settings.SMTP_HOST:
        raise RuntimeError("SMTP not configured")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_addr
    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    if settings.SMTP_USE_TLS:
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=30)
        server.ehlo()
        server.starttls()
        server.ehlo()
    else:
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=30)

    try:
        if settings.SMTP_USER:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_FROM, [to_addr], msg.as_string())
    finally:
        server.quit()


async def send_email(to_addr: str, subject: str, html_body: str, text_body: Optional[str] = None) -> bool:
    """
    Send an email. Returns True if sent (or simulated in dev), False on hard failure.
    When SMTP_HOST is empty, logs the message and returns True so flows can continue in dev.
    """
    settings = get_settings()
    text_body = text_body or ""

    if not settings.SMTP_HOST:
        logger.warning(
            "SMTP_HOST not set — email not sent. Subject=%s To=%s\n%s",
            subject,
            to_addr,
            text_body or html_body[:500],
        )
        return True

    try:
        await asyncio.to_thread(_send_sync, to_addr, subject, html_body, text_body)
        return True
    except Exception as e:
        logger.exception("Failed to send email to %s: %s", to_addr, e)
        return False
