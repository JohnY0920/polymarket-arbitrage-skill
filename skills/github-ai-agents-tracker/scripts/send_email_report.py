#!/usr/bin/env python3
"""
GitHub AI Agents Report Email Sender
Sends daily GitHub trending AI agents report via email
"""

import os
import sys
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def load_markdown_report():
    """Load the markdown report file"""
    today = datetime.now().strftime("%Y%m%d")
    report_file = f"ai_agents_{today}.md"
    
    if not os.path.exists(report_file):
        print(f"❌ Report file {report_file} not found")
        return None
    
    with open(report_file, 'r', encoding='utf-8') as f:
        return f.read()

def format_html_content(markdown_content):
    """Convert markdown to HTML for email"""
    # Simple markdown to HTML conversion
    html_content = markdown_content.replace('\n', '<br>')
    html_content = html_content.replace('**', '<strong>').replace('**', '</strong>')
    html_content = html_content.replace('*', '<em>').replace('*', '</em>')
    
    # Convert GitHub links to clickable URLs
    import re
    url_pattern = r'(https://github.com/[^\s]+)'
    html_content = re.sub(url_pattern, r'<a href="\1">\1</a>', html_content)
    
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background-color: #24292e; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .repo-item {{ margin-bottom: 30px; padding: 15px; border-left: 4px solid #0366d6; background-color: #f6f8fa; }}
            .repo-name {{ font-size: 18px; font-weight: bold; color: #0366d6; }}
            .repo-stats {{ color: #586069; font-size: 14px; margin: 5px 0; }}
            .repo-desc {{ margin-top: 10px; }}
            a {{ color: #0366d6; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🤖 Daily GitHub AI Agents Report</h1>
            <p>{datetime.now().strftime("%B %d, %Y")}</p>
        </div>
        <div class="content">
            {html_content}
        </div>
    </body>
    </html>
    """

def send_email(subject, html_content, recipients):
    """Send email via SMTP"""
    gmail_email = os.getenv('GMAIL_EMAIL')
    gmail_password = os.getenv('GMAIL_SMTP_PASSWORD')
    
    if not gmail_email or not gmail_password:
        print("❌ Email credentials not found in environment variables")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = gmail_email
        msg['To'] = ', '.join(recipients) if isinstance(recipients, list) else recipients
        
        # Add HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Connect to Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_email, gmail_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(gmail_email, recipients, text)
        server.quit()
        
        print(f"✅ Email sent successfully to {recipients}")
        return True
        
    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")
        return False

def main():
    """Main function"""
    print(f"🚀 Starting GitHub AI Agents Email Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load report
    markdown_content = load_markdown_report()
    if not markdown_content:
        print("❌ Could not load report")
        return False
    
    # Format HTML content
    html_content = format_html_content(markdown_content)
    
    # Get recipients from environment
    recipients_str = os.getenv('RECIPIENT_EMAIL', '')
    if not recipients_str:
        print("❌ No recipients found in RECIPIENT_EMAIL")
        return False
    
    recipients = [email.strip() for email in recipients_str.split(',')]
    
    # Send email
    subject = f"🤖 Daily GitHub AI Agents Report - {datetime.now().strftime('%B %d, %Y')}"
    success = send_email(subject, html_content, recipients)
    
    if success:
        print("✅ GitHub AI Agents email report completed successfully!")
    else:
        print("❌ GitHub AI Agents email report failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)