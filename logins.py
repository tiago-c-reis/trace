import firebase_admin
from firebase_admin import auth, credentials

import email_body
from credentials import credentials_values as cv

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import random
import string


cred = credentials.Certificate("./credentials/trace-rice-data-firebase-adminsdk-dl7fz-18df7c9b57.json")
firebase_admin.initialize_app(cred)


def create_user(email, password):
    """Create a new user"""
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return user.uid
    except Exception as e:
        return str(e)


def send_email(email, password):
    """Sends email to registered user"""

    # Sender and receiver email
    sender_address, sender_pass = cv.master.get('email'), cv.master.get('pw')
    receiver_address = email

    # HTML content
    mail_content = email_body.get_body(email, password)

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'TRACE-RICE | Account created successfully'

    # |-- email body
    message.attach(MIMEText(mail_content, 'html'))

    # Create SMTP session for sending the mail
    try:
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
    except smtplib.SMTPException as e:
        print("Error: unable to send email due to SMTPException", e)
    except Exception as e:
        print("Error: unable to send email due to ", str(e))


def generate_password():
    """Generates an x-length password"""
    all_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(all_characters) for i in range(10))


# ------------------------------------------------------------------------------
# Example:
# ------------------------------------------------------------------------------
user_email, user_password = 'info@materdynamics.com', generate_password()

uid = create_user(user_email, user_password)
r = send_email(user_email, user_password)

print(uid, r, sep='\n')

# ------------------------------------------------------------------------------
