#!/usr/bin/env python3
"""
Gamma Presentation Generator with Auto-Download and Email
Complete workflow: create → poll for completion → download → email attachment
"""

import os
import sys
import json
import requests
import smtplib
import time
import tempfile
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

def create_presentation_with_export(topic, research_data, format_type="pdf"):
    """Create presentation with export format specified"""
    
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
            initial_url = result.get("gammaUrl", "")
            status = result.get("status", "unknown")
            
            print(f"✅ Presentation created: {generation_id}")
            print(f"📊 Initial status: {status}")
            
            return {
                "success": True,
                "generation_id": generation_id,
                "initial_url": initial_url,
                "status": status,
                "message": "Presentation created successfully"
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
            "message": "Failed to create presentation"
        }

def wait_for_export_url(generation_id, format_type="pdf", max_wait=300, check_interval=15):
    """Poll API until export URL is available"""
    
    print(f"⏳ Polling for {format_type.upper()} export URL...")
    
    api_key = "sk-gamma-hClm0HmnAKp1Mo8oM1POPPVqPvJdbH4PJiOrxN8JzTk"
    base_url = "https://public-api.gamma.app/v1.0"
    
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": api_key,
        "User-Agent": "OpenClaw/1.0"
    }
    
    start_time = datetime.now()
    elapsed = 0
    
    while elapsed < max_wait:
        try:
            print(f"🔍 Checking status... ({elapsed}s elapsed)")
            
            response = requests.get(
                f"{base_url}/generations/{generation_id}",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                status = result.get("status", "unknown")
                gamma_url = result.get("gammaUrl", "")
                export_url = result.get("exportUrl", "")
                
                print(f"📊 Status: {status}")
                
                # Check if we have the export URL
                if export_url and export_url != "":
                    print(f"✅ Export URL found: {export_url[:50]}...")
                    return True, export_url, status
                
                # Check if presentation is ready
                elif status in ["completed", "done", "ready"]:
                    print(f"✅ Presentation completed!")
                    # Check file URLs endpoint as backup
                    file_result = get_file_urls_directly(generation_id, format_type)
                    if file_result["success"]:
                        return True, file_result["url"], status
                
                elif status in ["processing", "generating"]:
                    print(f"⏱️ Still processing... waiting {check_interval} seconds")
                    time.sleep(check_interval)
                    elapsed = (datetime.now() - start_time).total_seconds()
                
                else:
                    print(f"⚠️ Unexpected status: {status}")
                    time.sleep(check_interval)
                    elapsed = (datetime.now() - start_time).total_seconds()
                    
            else:
                print(f"❌ Status check failed: {response.status_code}")
                time.sleep(check_interval)
                elapsed = (datetime.now() - start_time).total_seconds()
                
        except Exception as e:
            print(f"❌ Status check error: {e}")
            time.sleep(check_interval)
            elapsed = (datetime.now() - start_time).total_seconds()
    
    print(f"⏰ Timeout reached after {max_wait} seconds")
    return False, "", "timeout"

def get_file_urls_directly(generation_id, format_type="pdf"):
    """Get file URLs using the file-urls endpoint"""
    
    api_key = "sk-gamma-hClm0HmnAKp1Mo8oM1POPPVqPvJdbH4PJiOrxN8JzTk"
    base_url = "https://public-api.gamma.app/v1.0"
    
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": api_key,
        "User-Agent": "OpenClaw/1.0"
    }
    
    try:
        print(f"📎 Getting file URLs for generation: {generation_id}")
        
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
                        return {
                            "success": True,
                            "url": url,
                            "format": format_type
                        }
            
            return {"success": False, "error": "Requested format not found"}
        else:
            return {"success": False, "error": f"File URLs endpoint returned {response.status_code}"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

def download_file(url, format_type):
    """Download the presentation file"""
    
    try:
        print(f"📥 Downloading {format_type.upper()} file...")
        
        response = requests.get(url, timeout=60)
        
        if response.status_code == 200:
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{format_type}") as tmp_file:
                tmp_file.write(response.content)
                print(f"✅ File downloaded: {tmp_file.name}")
                return tmp_file.name
        else:
            print(f"❌ Failed to download file: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Download error: {e}")
        return None

def create_and_email_presentation_with_attachment(topic, research_data, recipients, format_type="pdf"):
    """Complete workflow: create → poll → download → email with attachment"""
    
    print(f"🚀 Starting complete presentation workflow for: {topic}")
    
    # Step 1: Create presentation with export format
    create_result = create_presentation_with_export(topic, research_data, format_type)
    
    if not create_result["success"]:
        return create_result
    
    generation_id = create_result["generation_id"]
    
    # Step 2: Wait for export URL to be available
    print("\n" + "="*60)
    print("📋 STEP 2: Waiting for presentation to be ready...")
    print("="*60)
    
    success, export_url, final_status = wait_for_export_url(generation_id, format_type)
    
    if not success:
        print("⚠️ Export URL not available, will email with dashboard link")
        export_url = ""
    
    # Step 3: Download the file if available
    file_path = None
    if export_url and export_url != "":
        print("\n" + "="*60)
        print("📥 STEP 3: Downloading presentation file...")
        print("="*60)
        
        file_path = download_file(export_url, format_type)
    
    # Step 4: Create and send email
    print("\n" + "="*60)
    print("📧 STEP 4: Creating and sending email...")
    print("="*60)
    
    # Get email credentials
    gmail_email = os.getenv('GMAIL_EMAIL', 'wotb.spt@gmail.com')
    gmail_password = os.getenv('GMAIL_SMTP_PASSWORD', 'kaho mwqy nwyx sorq')
    
    # Create professional email (no platform mentions)
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
                <strong>Status:</strong> {'Ready with attachment' if file_path else 'Ready for viewing'}<br>
                <strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M")}
            </div>
            
            {f'<div style="text-align: center; margin: 30px 0;"><a href="{export_url if export_url else "#"}" class="button">📊 View Presentation</a></div>' if export_url else '<p><strong>Status:</strong> Presentation is ready for viewing.</p>'}
            
            {f'<p><strong>Download File:</strong></p><p>The {format_type.upper()} file is attached to this email.</p>' if file_path else ''}
            
            <div class="research-summary">
                <strong>Research Summary:</strong><br>
                {research_data[:400]}...
            </div>
            
            <p>This presentation includes comprehensive analysis, market insights, and actionable recommendations based on the latest research.</p>
        </div>
        
        <div class="footer">
            <p>Research Presentation System | Professional Analysis Generated</p>
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
            f'attachment; filename="{topic.replace(" ", "_")}_research_presentation.{format_type}"'
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
        "status": "ready" if file_path else "processing",
        "url": export_url if export_url else "Available in dashboard",
        "has_attachment": file_path is not None,
        "message": f"Presentation created and emailed to {recipients}"
    }

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 email_presentation_v3.py <topic> <research_data> <recipient_email> [format]")
        print("Example: python3 email_presentation_v3.py 'AI Trends' 'Research about AI...' 'user@example.com' pdf")
        sys.exit(1)
    
    topic = sys.argv[1]
    research_data = sys.argv[2]
    recipient = sys.argv[3]
    format_type = sys.argv[4] if len(sys.argv) > 4 else "pdf"
    
    result = create_and_email_presentation_with_attachment(topic, research_data, recipient, format_type)
    print(json.dumps(result, indent=2, ensure_ascii=False))