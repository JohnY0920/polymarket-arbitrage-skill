#!/usr/bin/env python3
"""
SMTP Email Sender for Executive News Digest
Uses Gmail SMTP instead of GOG for reliable delivery
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

class SMTPEmailSender:
    def __init__(self, sender_email=None, sender_password=None, recipients=None):
        self.sender_email = sender_email or os.environ.get('GMAIL_EMAIL', 'wotb.spt@gmail.com')
        self.sender_password = sender_password or os.environ.get('GMAIL_SMTP_PASSWORD')
        self.recipients = recipients or os.environ.get('RECIPIENT_EMAIL', 'johnyin@aisemble.ca')
        
        # Parse multiple recipients
        if isinstance(self.recipients, str):
            self.recipient_list = [email.strip() for email in self.recipients.split(',')]
        else:
            self.recipient_list = self.recipients if isinstance(self.recipients, list) else [self.recipients]
    
    def send_email(self, subject, body, html_body=None):
        """Send email via SMTP"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = ', '.join(self.recipient_list)
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            if html_body:
                msg.attach(MIMEText(html_body, 'html'))
            
            # Connect to SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            return True, "Email sent successfully"
            
        except Exception as e:
            return False, f"SMTP Error: {e}"
    
    def send_digest(self, subject, body, html_content=None):
        """Send the digest email"""
        return self.send_email(subject, body, html_content)
    
    def save_html_preview(self, english_content, chinese_content, file_path):
        """Save HTML preview (compatibility method)"""
        try:
            # Create HTML content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Executive News Digest Preview</title>
                <style>
                    body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                    h1 {{ color: #2c3e50; }}
                    h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                    .section {{ margin: 20px 0; }}
                    .commentary {{ background-color: #f8f9fa; padding: 15px; border-left: 4px solid #3498db; margin: 10px 0; }}
                </style>
            </head>
            <body>
                <h1>Executive News Digest</h1>
                <div class="section">
                    <h2>English Content</h2>
                    <div>{english_content}</div>
                </div>
                <div class="section">
                    <h2>Chinese Translation</h2>
                    <div>{chinese_content}</div>
                </div>
            </body>
            </html>
            """
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return True, f"HTML preview saved to {file_path}"
        except Exception as e:
            return False, f"Error saving HTML preview: {e}"