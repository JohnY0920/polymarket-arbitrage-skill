#!/usr/bin/env python3
"""
Gamma.app Presentation Creator
Create professional presentations using Gamma.app's AI-powered API.
"""

import json
import sys
import argparse
import requests
from datetime import datetime

def create_presentation(input_text, title=None, format="presentation", language="en", num_cards=13):
    """
    Create a presentation using Gamma API
    
    Args:
        input_text: Text content for the presentation
        title: Optional title override
        format: presentation, document, webpage, or social
        language: Output language
        num_cards: Number of slides/cards
    
    Returns:
        dict: API response with generation details
    """
    
    # Get API key from environment or use provided one
    api_key = "sk-gamma-hClm0HmnAKp1Mo8oM1POPPVqPvJdbH4PJiOrxN8JzTk"
    base_url = "https://public-api.gamma.app/v1.0"
    
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": api_key,
        "User-Agent": "OpenClaw/1.0"
    }
    
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
    
    if title:
        payload["title"] = title
    
    try:
        response = requests.post(
            f"{base_url}/generations",
            headers=headers,
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

def main():
    """Main function for CLI usage"""
    parser = argparse.ArgumentParser(description="Create presentations using Gamma.app API")
    
    parser.add_argument("--input", required=True, help="Text content for presentation")
    parser.add_argument("--title", help="Presentation title")
    parser.add_argument("--format", default="presentation", choices=["presentation", "document", "webpage", "social"], help="Output format")
    parser.add_argument("--language", default="en", help="Output language")
    parser.add_argument("--num-cards", type=int, default=13, help="Number of slides/cards")
    
    args = parser.parse_args()
    
    result = create_presentation(
        input_text=args.input,
        title=args.title,
        format=args.format,
        language=args.language,
        num_cards=args.num_cards
    )
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()