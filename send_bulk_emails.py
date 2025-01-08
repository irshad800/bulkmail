from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import tempfile
from email_validator import validate_email, EmailNotValidError

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

        # Convert recipients to a list
        recipient_list = [email.strip() for email in recipients.split(',')]

        # Validate recipient emails
        for email in recipient_list:
            try:
                validate_email(email)
            except EmailNotValidError as e:
                return jsonify({"error": f"Invalid email: {email}"}), 400

        # Send email to each recipient
        for recipient in recipient_list:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient
            msg['Subject'] = subject

            # Attach email body
            msg.attach(MIMEText(body, 'plain'))

            # Handle optional file attachment
            if 'cv' in request.files:
                file = request.files['cv']
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    file.save(tmp_file.name)
                    attachment = open(tmp_file.name, 'rb')
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f"attachment; filename={file.filename}")
                    msg.attach(part)
                    attachment.close()
                    os.unlink(tmp_file.name)

            # Send email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient, msg.as_string())

        return jsonify({"message": "Emails sent successfully"}), 200

    except smtplib.SMTPAuthenticationError:
        return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Use environment variable for port and bind to 0.0.0.0 for external access
    port = int(os.environ.get("PORT", 5000))  # Use the environment variable for port
    app.run(host="0.0.0.0", port=port, debug=True)
