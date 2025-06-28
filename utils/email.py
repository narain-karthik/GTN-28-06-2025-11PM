import smtplib
from email.mime.text import MIMEText
from flask import current_app


def send_assignment_email(to_email, ticket_id, assignee_name):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = current_app.config[
        'narainjkans@gmail.com']  # e.g., 'youraccount@gmail.com'
    smtp_password = current_app.config[
        'hefh vudq kkly wfsd']  # App password, not your Gmail login password

    subject = f"You have been assigned Ticket #{ticket_id}"
    body = f"Hello {assignee_name},\n\nYou have been assigned to Ticket #{ticket_id}. Please check the portal for details.\n\nBest regards,\nSupport Team"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, [to_email], msg.as_string())
