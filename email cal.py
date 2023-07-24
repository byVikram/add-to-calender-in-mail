import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from ics import Calendar, Event

def send_meeting_invitation(subject, message, recipients, start_time, end_time, location):
    # SMTP server configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'sender mail'
    smtp_password = 'password'

    # Create message container
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = ', '.join(recipients)

    # Create the HTML content of the email
    html_content = f'''
    <html>
        <body>
            <h2>{subject}</h2>
            <p>{message}</p>
            <p><a href="meeting.ics" download>Add to Calendar</a></p>
        </body>
    </html>
    '''

    # Create calendar event
    event = Event()
    event.name = subject
    event.begin = start_time
    event.end = end_time
    event.location = location

    # Create the .ics file
    cal = Calendar()
    cal.events.add(event)
    ics_file = 'meeting.ics'
    with open(ics_file, 'w') as f:
        f.writelines(cal)

    # Attach the HTML content to the email
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)

    # Attach the .ics file to the email
    ics_part = MIMEBase('text', 'calendar', method='REQUEST', name='meeting.ics')
    with open(ics_file, 'rb') as f:
        ics_part.set_payload(f.read())
    encoders.encode_base64(ics_part)
    ics_part.add_header('Content-Disposition', 'attachment; filename="meeting.ics"')
    msg.attach(ics_part)

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Send the email to all recipients
        server.sendmail(smtp_username, recipients, msg.as_string())
        server.quit()
        print('Meeting invitations sent successfully!')

        # Remove the .ics file
        os.remove(ics_file)
    except Exception as e:
        print(f'Error sending meeting invitations: {str(e)}')
        if os.path.exists(ics_file):
            os.remove(ics_file)

# Example usage
subject = 'Meeting Invitation'
message = 'You are invited to attend the meeting on June 20, 2023 at 08:00 AM.'
invitation='https://meet.google.com/zem-ajso-rvz'
recipients = ['receipient mail']
start_time = '2023-06-20 08:00:00'
end_time = '2023-06-20 09:00:00'
location = 'https://meet.google.com/zem-ajso-rvz'

send_meeting_invitation(subject, message, recipients, start_time, end_time, location)
