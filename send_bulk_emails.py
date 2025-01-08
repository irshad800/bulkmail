from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

app = Flask(__name__)
CORS(app)

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        # Get data from the request
        sender_email = request.form['your_email']
        sender_password = request.form['your_password']
        recipients = request.form['recipients']
        subject = request.form['subject']
        body = request.form['body']

        # Convert recipients to a list and format properly
        recipient_list = [email.strip() for email in recipients.split(',')]

        # Set up email headers and send separately for each recipient
        for recipient in recipient_list:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient  # Each email will have a unique recipient
            msg['Subject'] = subject

            # Attach email body
            msg.attach(MIMEText(body, 'plain'))

            # Handle optional file attachment
            if 'cv' in request.files:
                file = request.files['cv']
                filename = file.filename
                filepath = os.path.join('/tmp', filename)  # Temporary directory
                file.save(filepath)

                # Attach file to email
                attachment = open(filepath, 'rb')
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename={filename}")
                msg.attach(part)
                attachment.close()
                os.remove(filepath)  # Clean up temporary file

            # Send email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient, msg.as_string())

        return jsonify({"message": "Emails sent successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
