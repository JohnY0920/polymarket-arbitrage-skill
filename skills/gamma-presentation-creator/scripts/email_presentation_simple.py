#!/usr/bin/env python3
"""
Simple Gamma Presentation Email
Quick version without complex polling - sends email with initial link
"""

import os
import sys
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def create_and_email_simple(topic, research_data, recipients, format_type="pdf"):
    """Create presentation and email with initial link (no polling)"""
    
    api_key = "sk-gamma-hClm0HmnAKp1Mo8oM1POPPVqPvJdbH4PJiOrxN8JzTk"
    base_url = "https://public-api.gamma.app/v1.0"
    
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": api_key,
        "User-Agent": "OpenClaw/1.0"
    }
    
    print(f"🎨 Creating presentation about: {topic}")
    print(f"📄 Requesting {format_type.upper()} export format")
    
    # Build content
    content = f"""
    {topic}
    
    {research_data}
    
    This presentation covers key findings, market analysis, and practical applications.
    """
    
    # Create presentation with export format
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
        "exportAs": format_type,  # Request PDF/PPTX export
        "additionalInstructions": "Create a professional business presentation with clear sections, visual elements, and actionable insights."
    }
    
    try:
        response = requests.post(
            f"{base_url}/generations",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 201:
            result = response.json()
            generation_id = result.get("generationId")
            gamma_url = result.get("gammaUrl", "")
            status = result.get("status", "unknown")
            
            print(f"✅ Presentation created: {generation_id}")
            print(f"📊 Status: {status}")
            
            # Get email credentials
            gmail_email = os.getenv('GMAIL_EMAIL', 'wotb.spt@gmail.com')
            gmail_password = os.getenv('GMAIL_SMTP_PASSWORD', 'kaho mwqy nwyx sorq')
            
            # Create professional email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"📊 Research Presentation: {topic}"
            msg['From'] = gmail_email
            msg['To'] = recipients
            
            # Create email content
            html_content = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .header {{ background-color: #2C3E50; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; max-width: 600px; margin: 0 auto; }}
                    .button {{ display: inline-block; padding: 15px 30px; background-color: #3498DB; color: white; text-decoration: none; border-radius: 8px; margin: 20px 0; font-weight: bold; font-size: 16px; }}
                    .button:hover {{ background-color: #2980B9; }}
                    .info {{ background-color: #ecf0f1; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                    .footer {{ background-color: #34495e; color: white; padding: 15px; text-align: center; margin-top: 30px; }}
                    .research-summary {{ background-color: #f8f9fa; padding: 15px; border-left: 4px solid #3498DB; margin: 20px 0; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>📊 Research Presentation Ready</h1>
                    <p>{datetime.now().strftime("%B %d, %Y at %H:%M")}</p>
                </div>
                <div class="content">
                    <h2>{topic}</h2>
                    <p>A comprehensive research presentation has been prepared based on your requested topic.</p>
                    
                    <div class="info">
                        <strong>Topic:</strong> {topic}<br>
                        <strong>Status:</strong> {'Ready' if status in ['completed', 'done', 'ready'] else 'Processing - may take a few minutes'}<br>
                        <strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M")}
                    </div>
                    
                    {f'<div style="text-align: center; margin: 30px 0;"><a href="{gamma_url if gamma_url else "#"}" class="button">📊 View Presentation</a></div>' if gamma_url else '<p><strong>Status:</strong> Presentation is being prepared and will be available shortly.</p>'}
                    
                    <div class="research-summary">
                        <strong>Research Summary:</strong><br>
                        {research_data[:400]}...
                    </div>
                    
                    <p>This presentation includes comprehensive analysis, market insights, and actionable recommendations based on the latest research.</p>
                    
                    <p><strong>Next Steps:</strong></p>
                    <ul>
                        <li>Review the presentation for key insights</li>
                        <li>Check back in a few minutes if still processing</li>
                        <li>Contact us if you need any modifications</li>
                    </ul>
                </div>
                
                <div class="footer">
                    <p>Research Presentation System | Professional Analysis Generated</p>
                </div>
            </body>
            </html>
            """
            
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
            return {
                "success": True,
                "generation_id": generation_id,
                "format": format_type,
                "status": status,
                "url": gamma_url if gamma_url else "Will be available in dashboard",
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
        print("Usage: python3 email_presentation_simple.py <topic> <research_data> <recipient_email> [format]")
        print("Example: python3 email_presentation_simple.py 'AI Trends' 'Research about AI...' 'user@example.com' pdf")
        sys.exit(1)
    
    topic = sys.argv[1]
    research_data = sys.argv[2]
    recipient = sys.argv[3]
    format_type = sys.argv[4] if len(sys.argv) > 4 else "pdf"
    
    result = create_and_email_simple(topic, research_data, recipient, format_type)
    print(json.dumps(result, indent=2, ensure_ascii=False))