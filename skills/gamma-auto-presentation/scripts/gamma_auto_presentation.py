#!/usr/bin/env python3
"""
Gamma Auto Presentation Generator
Automatically creates presentations using Gamma.app API from research topics
"""

import os
import sys
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List, Optional

# Gamma API configuration
GAMMA_API_KEY = os.getenv('GAMMA_API_KEY', 'sk-gamma-hClm0HmnAKp1Mo8oM1POPPVqPvJdbH4PJiOrxN8JzTk')
# Try different API endpoints
GAMMA_API_BASES = [
    "https://api.gamma.app/v1",
    "https://ai.api.gamma.app/v1", 
    "https://gamma.app/api/v1"
]

class GammaAutoPresentation:
    def __init__(self):
        self.api_key = GAMMA_API_KEY
        self.api_bases = GAMMA_API_BASES
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'GammaAutoPresentation/1.0'
        }
    
    def test_api_connection(self) -> bool:
        """Test which API endpoint works"""
        print("🔍 Testing Gamma API endpoints...")
        
        for base_url in self.api_bases:
            try:
                # Test with a simple GET request
                response = requests.get(
                    f"{base_url}/user",
                    headers=self.headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    print(f"✅ API endpoint working: {base_url}")
                    self.base_url = base_url
                    return True
                else:
                    print(f"❌ {base_url}: {response.status_code} - {response.text[:100]}")
                    
            except Exception as e:
                print(f"❌ {base_url}: {str(e)[:100]}")
        
        return False
    
    def create_presentation(self, topic: str, content: str = "", presentation_type: str = "presentation", 
                          theme: str = "professional", language: str = "en") -> Dict:
        """Create a presentation using Gamma API"""
        
        if not hasattr(self, 'base_url'):
            if not self.test_api_connection():
                return {
                    "error": "Unable to connect to Gamma API. The API endpoints may have changed or require different authentication.",
                    "suggestion": "Please check Gamma's official documentation for the correct API endpoint and authentication method."
                }
        
        # Build the prompt for Gamma
        if not content:
            content = f"Create a comprehensive presentation about {topic}. Include key points, examples, and conclusions."
        
        payload = {
            "type": presentation_type,
            "theme": theme,
            "language": language,
            "content": content,
            "title": f"{topic} - Auto Generated",
            "description": f"Presentation about {topic} generated automatically"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/presentations",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            print(f"📊 API Response: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Presentation created: {result.get('id', 'unknown')}")
                return result
            else:
                print(f"❌ API Error: {response.status_code} - {response.text[:200]}")
                return {
                    "error": f"API returned {response.status_code}",
                    "details": response.text[:200],
                    "suggestion": "The API endpoint or authentication method may have changed. Please check Gamma's documentation."
                }
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
            return {
                "error": str(e),
                "suggestion": "Check network connectivity and API availability"
            }
    
    def generate_from_research(self, research_topic: str, research_data: str = "", 
                             format_type: str = "presentation") -> Dict:
        """Generate presentation from research data"""
        
        content = f"""
        Research Topic: {research_topic}
        
        {research_data if research_data else f"Please create a comprehensive presentation about {research_topic} covering key concepts, recent developments, and practical applications."}
        
        Include:
        - Executive summary
        - Key findings
        - Visual elements and charts
        - Conclusions and next steps
        """
        
        return self.create_presentation(
            topic=research_topic,
            content=content,
            presentation_type=format_type
        )
    
    def save_result(self, result: Dict, output_dir: str = "../output") -> str:
        """Save the presentation result to file"""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gamma_presentation_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Saved result to {filepath}")
        return filepath
    
    def send_email(self, presentation_result: Dict, recipients: List[str]) -> bool:
        """Send presentation via email"""
        
        gmail_email = os.getenv('GMAIL_EMAIL')
        gmail_password = os.getenv('GMAIL_SMTP_PASSWORD')
        
        if not gmail_email or not gmail_password:
            print("❌ Email credentials not found")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🎨 Gamma Presentation: {presentation_result.get('title', 'Auto Generated')}"
            msg['From'] = gmail_email
            msg['To'] = ', '.join(recipients)
            
            # Create email content
            presentation_url = presentation_result.get('public_url', '')
            title = presentation_result.get('title', 'Auto Generated Presentation')
            
            html_content = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .header {{ background-color: #6C5CE7; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; }}
                    .button {{ display: inline-block; padding: 12px 24px; background-color: #6C5CE7; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🎨 New Gamma Presentation Generated!</h1>
                    <p>{datetime.now().strftime("%B %d, %Y at %H:%M")}</p>
                </div>
                <div class="content">
                    <h2>{title}</h2>
                    <p>A new presentation has been automatically generated using Gamma.app AI.</p>
                    
                    {f'<p><strong>View Presentation:</strong></p><p><a href="{presentation_url}" class="button">Open Presentation</a></p>' if presentation_url else '<p><strong>Status:</strong> Presentation is being processed and will be available shortly.</p>'}
                    
                    <p><strong>Generated by:</strong> OpenClaw AI Automation</p>
                    <p>This presentation was created automatically based on your research topic.</p>
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
            return True
            
        except Exception as e:
            print(f"❌ Email sending failed: {e}")
            return False

def main():
    """Main function for CLI usage"""
    if len(sys.argv) < 2:
        print("Usage: python3 gamma_auto_presentation.py <topic> [research_data] [recipients]")
        print("\nExample:")
        print("  python3 gamma_auto_presentation.py \"AI Agents Overview\"")
        print("  python3 gamma_auto_presentation.py \"AI Agents Overview\" \"Research data here...\" \"user@example.com\"")
        sys.exit(1)
    
    topic = sys.argv[1]
    research_data = sys.argv[2] if len(sys.argv) > 2 else ""
    recipients_str = sys.argv[3] if len(sys.argv) > 3 else os.getenv('RECIPIENT_EMAIL', '')
    
    if recipients_str:
        recipients = [email.strip() for email in recipients_str.split(',')]
    else:
        recipients = []
    
    # Create presentation
    generator = GammaAutoPresentation()
    result = generator.generate_from_research(topic, research_data)
    
    if "error" not in result:
        # Save result
        generator.save_result(result)
        
        # Send email if recipients provided
        if recipients:
            generator.send_email(result, recipients)
        
        print("✅ Presentation generation completed!")
        print(f"📊 Presentation ID: {result.get('id', 'unknown')}")
        print(f"🔗 URL: {result.get('public_url', 'processing...')}")
    else:
        print("❌ Presentation generation failed!")
        print(f"Error: {result.get('error', 'Unknown error')}")
        if "suggestion" in result:
            print(f"Suggestion: {result['suggestion']}")
        sys.exit(1)

if __name__ == "__main__":
    main()