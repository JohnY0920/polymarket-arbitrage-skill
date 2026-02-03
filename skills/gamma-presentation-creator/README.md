# Gamma Presentation Creator Skill

Create professional presentations and documents using Gamma.app's AI-powered API.

## 🎯 Overview

This skill integrates Gamma.app's API to create polished presentations, documents, websites, and social media content from text. Perfect for business presentations, pitch decks, investor materials, and multilingual content.

## ✨ Features

- **Text-to-Presentation** - Convert ideas to professional slides
- **Multiple Formats** - Presentations, documents, websites, social media
- **Multilingual Support** - 60+ languages including Chinese, English, etc.
- **Professional Themes** - Business-ready designs
- **Export Options** - PDF, PPTX, direct sharing
- **Template Support** - Use professional templates

## 🚀 Quick Start

### Prerequisites

1. **Get Gamma API Key**
   - Visit https://gamma.app
   - Sign up for account
   - Go to Settings → API
   - Generate API key

2. **Install Dependencies**
   ```bash
   pip install requests
   ```

### Basic Usage

```bash
# Create presentation from text
python scripts/gamma_creator.py \
  --input "Your presentation content" \
  --title "Your Title" \
  --format presentation \
  --language zh

# List available themes
python scripts/gamma_creator.py --list-themes

# Get download URLs
python scripts/gamma_creator.py --get-urls "generation-id-here"
```

## 📁 Structure

```
gamma-presentation-creator/
├── SKILL.md                                    # Main skill documentation
├── README.md                                   # This file
├── scripts/
│   ├── gamma_creator.py                        # Main API integration script
│   └── chinese_tech_canada_presentation.py     # Specific presentation content
└── references/
    └── gamma_api.md                            # API documentation
```

## 🎨 Example: Chinese Tech Company Presentation

The skill includes a pre-built 13-slide presentation about Chinese tech companies expanding to Canada:

```python
# Content is already prepared in:
scripts/chinese_tech_canada_presentation.py
```

**Topics covered:**
1. Cover slide - Canada as optimal springboard
2. Current trends - 200+ Chinese tech companies
3. Global perspective - Canada ecosystem ranking
4. Core challenges - US barriers, Singapore limitations
5. Canada solution - Trusted identity, global access, smart ecosystem
6. Cost analysis - 46% savings vs Silicon Valley
7. Geopolitical window - 2026 golden opportunity
8. Real cases - Cohere, Wealthsimple, anonymous Chinese AI company
9. Clear path - Timeline and milestones
10. Target companies - B2B SaaS, AI/ML, Fintech, Healthtech
11. Key data summary
12. Next steps
13. Contact information

## 🛠️ API Configuration

**Edit `gamma_creator.py` to add your API key:**

```python
def _get_api_key(self):
    """Get API key from config or environment"""
    return "YOUR_GAMMA_API_KEY_HERE"  # Replace with your actual key
```

Or set environment variable:
```bash
export GAMMA_API_KEY="your-key-here"
```

## 📊 API Endpoints Used

- **POST** `/v1.0/generations` - Create presentation
- **POST** `/v1.0/create-from-template` - Use template
- **GET** `/v1.0/generations/{id}/file-urls` - Get downloads
- **GET** `/v1.0/themes` - List themes

## 🌍 Supported Languages

Chinese (zh), English (en), French (fr), German (de), Japanese (ja), Spanish (es), Korean (ko), and 50+ more.

## 💡 Use Cases

### Business Presentations
```bash
python scripts/gamma_creator.py \
  --input "Market analysis for Q4..." \
  --title "Q4 Business Review" \
  --format presentation \
  --language en
```

### Investor Pitch Decks
```bash
python scripts/gamma_creator.py \
  --input "AI startup solving healthcare..." \
  --title "ABC Corp - Series A Pitch" \
  --format presentation \
  --num-cards 15
```

### Multilingual Content
```bash
python scripts/gamma_creator.py \
  --input "中国科技企业出海策略..." \
  --title "全球化战略" \
  --format presentation \
  --language zh
```

## 🔧 Integration with OpenClaw

In Clawdbot, just ask:
```
"Create a Gamma presentation about [topic]"
"Make a pitch deck for [company]"
"Convert this to slides: [your text]"
```

## 📝 Notes

- API responses are asynchronous (polling may be needed)
- Generated content appears in Gamma dashboard
- File URLs expire after certain time
- Free tier has rate limits (250k tokens/min)

## 🔗 Resources

- **Gamma.app:** https://gamma.app
- **API Docs:** https://developers.gamma.app
- **Support:** Check references/gamma_api.md

## 📄 License

Part of OpenClaw/Clawdbot skill ecosystem.

---

**Ready to create professional presentations with AI!** 🚀
