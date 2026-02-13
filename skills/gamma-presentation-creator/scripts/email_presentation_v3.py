#!/usr/bin/env python3
"""
Presentation Generator with Status Monitoring and Better Email
Waits for generation to complete and sends professional emails with working links
"""

import os
import sys
import json
import requests
import smtplib
import time
import tempfile
import urllib.request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

def check_generation_status(generation_id):
    """Check if presentation generation is complete"""
    
    api_key = "sk-gamma-hClm0HmnAKp1Mo8oM1POPPVqPvJdbH4PJiOrxN8JzTk"
    base_url = "https://public-api.gamma.app/v1.0"
    
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": api_key,
        "User-Agent": "OpenClaw/1.0"
    }
    
    try:
        response = requests.get(
            f"{base_url}/generations/{generation_id}",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            status = result.get("status", "unknown")
            gamma_url = result.get("gammaUrl", "")
            
            print(f"📊 Generation status: {status}")
            
            # Check if it's ready
            if status in ["complete", "done", "ready"] and gamma_url:
                return True, gamma_url, status
            elif status in ["processing", "generating"]:
                return False, gamma_url, status
            else:
                return False, gamma_url, status
                
        else:
            print(f"❌ Status check failed: {response.status_code}")
            return False, "", "error"
            
    except Exception as e:
        print(f"❌ Status check error: {e}")
        return False, "", "error"

def wait_for_completion(generation_id, max_wait=300, check_interval=10):
    """Wait for presentation to be ready"""
    print(f"⏳ Waiting for presentation to be ready...")
    
    start_time = datetime.now()
    elapsed = 0
    
    while elapsed < max_wait:
        is_ready, url, status = check_generation_status(generation_id)
        
        if is_ready:
            print(f"✅ Presentation is ready!")
            return True, url
        elif status in ["processing", "generating"]:
            print(f"⏱️ Still processing... ({elapsed}s elapsed)")
            time.sleep(check_interval)
            elapsed = (datetime.now() - start_time).total_seconds()
        else:
            print(f"⚠️ Unexpected status: {status}")
            return False, ""
    
    print(f"⏰ Timeout reached after {max_wait} seconds")
    return False, ""

def create_and_email_presentation(topic, research_data, recipients, format_type="pdf"):
    """Create presentation and email it with proper status monitoring"""
    
    # API configuration
    api_key = "sk-gamma-hClm0HmnAKp1Mo8oM1POPPVqPvJdbH4PJiOrxN8JzTk"
    base_url = "https://public-api.gamma.app/v1.0"
    
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": api_key,
        "User-Agent": "OpenClaw/1.0"
    }
    
    try:
        print(f"🎨 Creating presentation about: {topic}")
        
        # Build content
        content = f"""
        {topic}
        
        {research_data}
        
        This presentation covers key findings, market analysis, and practical applications.
        """
        
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
            initial_url = result.get("gammaUrl", "")
            print(f"✅ Presentation created: {generation_id}")
            
            # Wait for completion
            print("⏳ Waiting for presentation to be ready...")
            is_ready, final_url = wait_for_completion(generation_id)
            
            if not is_ready:
                print("⚠️ Presentation is still processing, will email with current link")
                final_url = initial_url
            
            # Get email credentials
            gmail_email = os.getenv('GMAIL_EMAIL', 'wotb.spt@gmail.com')
            gmail_password = os.getenv('GMAIL_SMTP_PASSWORD', 'kaho mwqy nwyx sorq')
            
            # Create professional email (no platform mentions)
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"📊 Research Presentation: {topic}"
            msg['From'] = gmail_email
            msg['To'] = recipients
            
            # Create proper HTML email with working links
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
                        <strong>Status:</strong> {'Ready for viewing' if is_ready else 'Processing - may take a few more minutes'}<br>
                        <strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M")}
                    </div>
                    
                    {f'<div style="text-align: center; margin: 30px 0;"><a href="{final_url}" class="button">📊 View Presentation</a></div>' if final_url else '<p><strong>Status:</strong> Presentation is being prepared and will be available shortly.</p>'}
                    
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
                "status": "ready" if is_ready else "processing",
                "url": final_url if final_url else "Will be available in dashboard",
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
        print("Usage: python3 email_presentation_v2.py <topic> <research_data> <recipient_email> [format]")
        print("Example: python3 email_presentation_v2.py 'AI Trends' 'Research about AI...' 'user@example.com' pdf")
        sys.exit(1)
    
    topic = sys.argv[1]
    research_data = sys.argv[2]
    recipient = sys.argv[3]
    format_type = sys.argv[4] if len(sys.argv) > 4 else "pdf"
    
    result = create_and_email_presentation(topic, research_data, recipient, format_type)
    print(json.dumps(result, indent=2, ensure_ascii=False))