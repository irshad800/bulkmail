import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

# Email credentials
your_email = "irshadvp800@gmail.com"
your_password = "tlespnxtafrtjzou"  # Your Gmail App Password

# Get the current date
current_date = datetime.now().strftime("%A, %B %d, %Y")

# Email content
subject = "Application for IT Specialist Position"
body = f"""
Deira, Dubai
Mobile: 0563020773
Email: irshadvp800@gmail.com
LinkedIn: linkedin.com/in/muhammed-irshad-vp-0a9648247
Portfolio: irshad800.github.io/prtfolio
GitHub: github.com/irshad800

Date: {current_date}

Dear Hiring Manager,

I am thrilled to apply for the IT Specialist position at your esteemed company. With a Master’s in Computer Applications (MCA) from KTU and a Bachelor’s in Computer Science from Calicut University, I bring a strong academic foundation combined with hands-on experience in software and hardware systems. Over the past seven months, I have developed and delivered seven high-quality projects, including five full-stack applications that span domains like e-commerce, healthcare, and optical store management. My technical expertise in Flutter, Node.js, and MongoDB, coupled with a deep understanding of REST API integration and state management using Provider and BLoC, makes me well-equipped to tackle complex IT challenges.

Beyond my software development skills, I have a knack for bridging hardware and software functionalities, ensuring seamless integration to meet user and business requirements. Notable achievements include designing an eCommerce app with advanced cart and checkout features, building an Ayurvedic patient management system with PDF generation, and delivering intuitive UI/UX solutions. I take pride in my ability to problem-solve, adapt to dynamic project needs, and collaborate effectively within teams. Joining your company represents an exciting opportunity to contribute to innovative projects and drive impactful IT solutions.

Thank you for considering my application. I look forward to the opportunity to discuss how my background aligns with your requirements. Please feel free to reach out at 0563020773 or via email at irshadvp800@gmail.com.

Sincerely,
Muhammed Irshad VP
"""

# List of recipients
recipients = [
   "farshadvp772@gmail.com"
]

# Path to your CV file
cv_path = "M.IRSHAD PROFILE.pdf"  # Replace with the actual path to your CV

# Sending email
for recipient in recipients:
    try:
        # Email setup
        msg = MIMEMultipart()
        msg['From'] = your_email
        msg['To'] = recipient
        msg['Subject'] = subject

        # Attach body text
        msg.attach(MIMEText(body, 'plain'))

        # Attach CV
        with open(cv_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={cv_path.split('/')[-1]}"
            )
            msg.attach(part)

        # Connect to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(your_email, your_password)

        # Send email
        server.sendmail(your_email, recipient, msg.as_string())
        print(f"Email sent successfully to {recipient}")

        # Close the server
        server.quit()
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")  