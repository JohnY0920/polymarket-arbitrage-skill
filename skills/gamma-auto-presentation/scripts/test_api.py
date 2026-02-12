#!/usr/bin/env python3
"""
Test script for Gamma Auto Presentation skill
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.gamma_auto_presentation import GammaAutoPresentation

def test_api_connection():
    """Test Gamma API connection"""
    print("🧪 Testing Gamma API connection...")
    
    # Set API key
    os.environ['GAMMA_API_KEY'] = 'sk-gamma-hClm0HmnAKp1Mo8oM1POPPVqPvJdbH4PJiOrxN8JzTk'
    
    generator = GammaAutoPresentation()
    
    # Test simple presentation creation
    result = generator.create_presentation(
        topic="AI Agents Overview",
        content="This is a test presentation about AI agents and their applications in 2024.",
        presentation_type="presentation",
        theme="professional"
    )
    
    if "error" not in result:
        print("✅ Gamma API connection successful!")
        print(f"📊 Presentation ID: {result.get('id', 'unknown')}")
        print(f"🔗 URL: {result.get('public_url', 'processing...')}")
        return True
    else:
        print(f"❌ API test failed: {result['error']}")
        return False

if __name__ == "__main__":
    success = test_api_connection()
    sys.exit(0 if success else 1)