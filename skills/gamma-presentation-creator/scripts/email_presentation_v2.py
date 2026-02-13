#!/usr/bin/env python3
"""
Presentation Generator with Email & File Attachment
Create presentations and email them with actual file attachments
"""

import os
import sys
import json
import requests
import smtplib
import tempfile
import urllib.request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

def get_presentation_file(generation_id, format_type="pdf"):
    """Get the actual presentation file from Gamma API"""
    
    api_key = "sk-gamma-hClm0HmnAKp1Mo8oM1POPPVqPvJdbH4PJiOrxN8JzTk"
    base_url = "https://public-api.gamma.app/v1.0"
    
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": api_key,
        "User-Agent": "OpenClaw/1.0"
    }
    
    try:
        print(f"📎 Getting file URLs for generation: {generation_id}")
        
        # Get file URLs
        response = requests.get(
            f"{base_url}/generations/{generation_id}/file-urls",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            file_urls = result.get("fileUrls", [])
            
            # Find the requested format
            for file_info in file_urls:
                if file_info.get("format") == format_type:
                    url = file_info.get("url")
                    if url:
                        print(f"📥 Downloading {format_type.upper()} file...")
                        
                        # Download the file
                        file_response = requests.get(url, timeout=60)
                        if file_response.status_code == 200:
                            # Save to temporary file
                            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{format_type}") as tmp_file:
                                tmp_file.write(file_response.content)
                                print(f"✅ File downloaded: {tmp_file.name}")
                                return tmp_file.name
                        else:
                            print(f"❌ Failed to download file: {file_response.status_code}")
            
            print("⚠️ No suitable file format found, will email link instead")
            return None
            
        else:
            print(f"❌ Failed to get file URLs: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error getting file: {e}")
        return None

def create_and_email_presentation(topic, research_data, recipients, format_type="pdf"):
    """Create presentation and email it with file attachment"""
    
    # API configuration
    api_key = "sk-gamma-hClm0HmnAKp1Mo8oM1POPPVqPvJdbH4PJiOrxN8JzTk"
    base_url = "https://public-api.gamma.app/v1.0"
    
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": api_key,
        "User-Agent": "OpenClaw/1.0"
    }
    
    # Build content
    content = f"""
    {topic}
    
    {research_data}
    
    This presentation covers key findings, market analysis, and practical applications.
    """
    
    try:
        print(f"🎨 Creating presentation about: {topic}")
        
        # Create presentation
        payload = {
            "inputText": content,
            "textMode": "generate",
            "format": "presentation",
            "textOptions": {
                "language": "en",
                "tone": "professional"
            },
            "numCards": 13,
            "cardSplit": "auto",
            "exportAs": format_type,  # Request specific format
            "additionalInstructions": "Create a professional business presentation with clear sections, visual elements, and actionable insights."
        }
        
        response = requests.post(
            f"{base_url}/generations",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 201:
            result = response.json()
            generation_id = result.get("generationId")
            gamma_url = result.get("gammaUrl")
            print(f"✅ Presentation created: {generation_id}")
            
            # Get the actual file
            print("📎 Getting presentation file...")
            file_path = get_presentation_file(generation_id, format_type)
            
            # Get email credentials
            gmail_email = os.getenv('GMAIL_EMAIL', 'wotb.spt@gmail.com')
            gmail_password = os.getenv('GMAIL_SMTP_PASSWORD', 'kaho mwqy nwyx sorq')
            
            # Create email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"📊 Research Presentation: {topic}"
            msg['From'] = gmail_email
            msg['To'] = recipients
            
            # Create email content (no mention of Gamma)
            html_content = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .header {{ background-color: #2C3E50; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; }}
                    .button {{ display: inline-block; padding: 12px 24px; background-color: #3498DB; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                    .info {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                    .footer {{ background-color: #34495e; color: white; padding: 10px; text-align: center; margin-top: 30px; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>📊 Research Presentation</h1>
                    <p>{datetime.now().strftime("%B %d, %Y at %H:%M")}</p>
                </div>
                <div class="content">
                    <h2>{topic}</h2>
                    <p>A comprehensive research presentation has been prepared based on your requested topic.</p>
                    
                    <div class="info">
                        <strong>Topic:</strong> {topic}<br>
                        <strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M")}<br>
                        <strong>Format:</strong> {format_type.upper()}
                    </div>
                    
                    {f'<p><strong>Download Presentation:</strong></p><p>The presentation file is attached to this email.</p>' if file_path else f'<p><strong>Access Presentation:</strong></p><p><a href="{gamma_url}" class="button">View Presentation Online</a></p>'}
                    
                    <p><strong>Research Summary:</strong></p>
                    <p>{research_data[:300]}...</p>
                    
                    <p>This presentation includes comprehensive analysis, market insights, and actionable recommendations based on the latest research.</p>
                </div>
                
                <div class="footer">
                    <p>Research Presentation System | Generated automatically based on your request</p>
                </div>
            </body>
            </html>
            """
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Attach file if we got it
            if file_path:
                print(f"📎 Attaching {format_type.upper()} file...")
                
                with open(file_path, 'rb') as f:
                    part = MIMEBase('application', f'octet-stream')
                    part.set_payload(f.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{topic.replace(" ", "_")}_presentation.{format_type}"'
                )
                msg.attach(part)
                
                # Clean up temporary file
                os.unlink(file_path)
            
            # Connect to Gmail SMTP
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_email, gmail_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(gmail_email, recipients, text)
            server.quit()
            
            print(f"✅ Email sent successfully to {recipients}")
            return {
                "success": True,
                "generation_id": generation_id,
                "format": format_type,
                "message": f"Presentation created and emailed to {recipients}"
            }
            
        else:
            print(f"❌ API Error: {response.status_code} - {response.text[:200]}")
            return {
                "success": False,
                "error": f"API returned {response.status_code}",
                "message": "Failed to create presentation"
            }
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create and email presentation"
        }

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 email_presentation.py <topic> <research_data> <recipient_email> [format]")
        print("Example: python3 email_presentation.py 'AI Trends' 'Research about AI...' 'user@example.com' pdf")
        sys.exit(1)
    
    topic = sys.argv[1]
    research_data = sys.argv[2]
    recipient = sys.argv[3]
    format_type = sys.argv[4] if len(sys.argv) > 4 else "pdf"
    
    result = create_and_email_presentation(topic, research_data, recipient, format_type)
    print(json.dumps(result, indent=2, ensure_ascii=False))