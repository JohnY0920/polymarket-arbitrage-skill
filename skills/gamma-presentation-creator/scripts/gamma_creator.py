#!/usr/bin/env python3
"""
Gamma.app Presentation Creator for OpenClaw/Clawdbot

Create professional presentations using Gamma.app's AI-powered API.
Supports multiple formats, templates, and languages.

Usage:
    python gamma_creator.py --input "presentation text" --title "Title" --format presentation
    python gamma_creator.py --template "Tech Startup Pitch" --company "ABC Corp" --format presentation
"""

import json
import sys
import argparse
import requests
from datetime import datetime
from pathlib import Path

class GammaPresentationCreator:
    def__init__(self, api_key=None):
        """
        Initialize Gamma Presentation Creator
        
        Args:
            api_key: Gamma.app API key (if not provided, uses config)
        """
        self.api_key = api_key or self._get_api_key()
        self.base_url = "https://public-api.gamma.app/v1.0"
        self.headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key,
            "User-Agent": "OpenClaw/1.0"
        }
    
    def _get_api_key(self):
        """Get API key from config or environment"""
        # In real implementation, this would read from config
        return "YOUR_GAMMA_API_KEY_HERE"
    
    def create_presentation(self, input_text, title=None, format="presentation", 
                          theme_id=None, num_cards=13, language="zh"):
        """
        Create a presentation using Gamma API
        
        Args:
            input_text: Text content for the presentation
            title: Optional title override
            format: presentation, document, webpage, or social
            theme_id: Optional theme ID
            num_cards: Number of slides/cards (default 13)
            language: Output language (default Chinese)
        
        Returns:
            dict: API response with generation details
        """
        
        payload = {
            "inputText": input_text,
            "textMode": "generate",
            "format": format,
            "textOptions": {
                "language": language,
                "tone": "professional"
            },
            "numCards": num_cards,
            "cardSplit": "auto",
            "additionalInstructions": f"Create a professional {format} in {language}. Use clear, business-appropriate design."
        }
        
        if theme_id:
            payload["themeId"] = theme_id
            
        if title:
            payload["title"] = title
            
        try:
            response = requests.post(
                f"{self.base_url}/generations",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 201:
                result = response.json()
                return {
                    "success": True,
                    "generation_id": result.get("generationId"),
                    "status": result.get("status"),
                    "url": result.get("gammaUrl"),
                    "message": "Presentation created successfully"
                }
            else:
                return {
                    "success": False,
                    "error": f"API returned {response.status_code}: {response.text}",
                    "message": "Failed to create presentation"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Network error creating presentation"
            }
    
    def create_from_template(self, template_id, company_name, format="presentation", 
                           language="zh"):
        """
        Create presentation from existing template
        
        Args:
            template_id: Gamma template ID
            company_name: Company name to insert
            format: Output format
            language: Output language
            
        Returns:
            dict: API response
        """
        payload = {
            "templateId": template_id,
            "companyName": company_name,
            "format": format,
            "textOptions": {
                "language": language
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/create-from-template",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 201:
                result = response.json()
                return {
                    "success": True,
                    "generation_id": result.get("generationId"),
                    "status": result.get("status"),
                    "url": result.get("gammaUrl"),
                    "message": "Template presentation created successfully"
                }
            else:
                return {
                    "success": False,
                    "error": f"API returned {response.status_code}: {response.text}",
                    "message": "Failed to create from template"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Network error creating from template"
            }
    
    def get_file_urls(self, generation_id):
        """
        Get download URLs for generated presentation
        
        Args:
            generation_id: The ID from create_presentation()
            
        Returns:
            dict: File URLs and download information
        """
        try:
            response = requests.get(
                f"{self.base_url}/generations/{generation_id}/file-urls",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "file_urls": result.get("fileUrls", []),
                    "formats": result.get("formats", []),
                    "message": "File URLs retrieved successfully"
                }
            else:
                return {
                    "success": False,
                    "error": f"API returned {response.status_code}: {response.text}",
                    "message": "Failed to get file URLs"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Network error getting file URLs"
            }
    
    def list_themes(self):
        """
        List available themes from Gamma
        
        Returns:
            dict: Available themes
        """
        try:
            response = requests.get(
                f"{self.base_url}/themes",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "themes": result.get("themes", []),
                    "message": "Themes retrieved successfully"
                }
            else:
                return {
                    "success": False,
                    "error": f"API returned {response.status_code}: {response.text}",
                    "message": "Failed to get themes"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Network error getting themes"
            }

def main():
    """Main function for CLI usage"""
    parser = argparse.ArgumentParser(description="Create presentations using Gamma.app API")
    
    parser.add_argument("--input", required=True, help="Text content for presentation")
    parser.add_argument("--title", help="Presentation title")
    parser.add_argument("--format", default="presentation", choices=["presentation", "document", "webpage", "social"], help="Output format")
    parser.add_argument("--language", default="zh", help="Output language")
    parser.add_argument("--num-cards", type=int, default=13, help="Number of slides/cards")
    parser.add_argument("--template", help="Use specific template ID")
    parser.add_argument("--theme-id", help="Use specific theme ID")
    parser.add_argument("--list-themes", action="store_true", help="List available themes")
    parser.add_argument("--get-urls", help="Get file URLs for generation ID")
    
    args = parser.parse_args()
    
    creator = GammaPresentationCreator()
    
    if args.list_themes:
        result = creator.list_themes()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.get_urls:
        result = creator.get_file_urls(args.get_urls)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.template:
        result = creator.create_from_template(args.template, args.input, args.format, args.language)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        result = creator.create_presentation(
            input_text=args.input,
            title=args.title,
            format=args.format,
            language=args.language,
            num_cards=args.num_cards,
            theme_id=args.theme_id
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
"