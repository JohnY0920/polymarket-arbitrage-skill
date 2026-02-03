---
name: gamma-presentation-creator
description: Create professional presentations and documents using Gamma.app's AI-powered API. Convert ideas, text, or structured content into polished presentations, documents, websites, or social media content. Supports multiple languages, themes, and export formats. Perfect for business presentations, pitch decks, reports, and multilingual content creation. Use when you need to create professional presentations from text, convert business ideas into slides, or generate polished documents for investors, clients, or stakeholders.
---

# Gamma Presentation Creator

Create professional presentations and documents using Gamma.app's AI-powered API.

## 🎯 What This Does

Converts your ideas, text, or structured content into polished presentations, documents, websites, or social media content using Gamma's AI. Perfect for:
- Business presentations and pitch decks
- Investor reports and documents  
- Multilingual business content
- Professional documents from text
- AI-powered content creation

**Data Source:** Gamma.app API (https://gamma.app/)

## 🚀 Quick Start

### Basic Usage

```bash
# Create presentation from text
python scripts/gamma_creator.py --input "Your presentation content" --title "Your Title" --format presentation --language zh

# Use template
python scripts/gamma_creator.py --template "template-123" --company "Your Company" --format presentation --language zh

# Get available themes
python scripts/gamma_creator.py --list-themes
```

### In Clawdbot

Just ask me to create a presentation:

```
"Create a Gamma presentation about [topic]"
"Make a professional pitch deck for [company/industry]"
"Convert this text into slides: [your text]"
"Create a presentation in Chinese about [topic]"
```

## 📋 Features

### Content Creation
- **Text to Presentation** - Convert any text to slides
- **Template Integration** - Use professional templates
- **Multiple Languages** - Support for 60+ languages
- **Multiple Formats** - Presentations, documents, websites, social media

### Professional Output
- **AI-Powered Design** - Automatic layout and design
- **Consistent Branding** - Professional themes and styling
- **Export Options** - PDF, PPTX, direct sharing
- **Multilingual Support** - Perfect for international business

### Business Integration
- **Investor-Ready** - Professional pitch deck formatting
- **Market Analysis** - Data-driven presentations
- **B2B Focus** - Enterprise and business presentations
- **Global Markets** - Content for international audiences

## 🛠️ Components

### scripts/gamma_creator.py
Main script for Gamma API interaction with all creation functions

### references/gamma_api.md
Complete API documentation and integration guide

### Built-in Templates
Professional business templates for various use cases

## 🎯 Use Cases

### 1. Business Presentations
```bash
# Investor pitch deck
python scripts/gamma_creator.py --input "Our AI company raised $5M..." --title "ABC Corp Investor Deck" --format presentation --language en

# Market analysis report
python scripts/gamma_creator.py --input "Canadian tech market analysis..." --title "Market Entry Strategy" --format document --language en
```

### 2. Multilingual Content
```bash
# Chinese business presentation
python scripts/gamma_creator.py --input "中国科技企业出海策略..." --title "全球化战略" --format presentation --language zh

# International investor materials
python scripts/gamma_creator.py --input "Market opportunity analysis..." --title "Global Expansion" --format presentation --language en
```

### 3. Specific Business Needs
```bash
# Tech startup pitch
python scripts/gamma_creator.py --input "Our AI/ML platform..." --title "Tech Startup Pitch" --format presentation --language en

# Government report
python scripts/gamma_creator.py --input "Policy analysis and recommendations..." --title "Government Report" --format document --language en
```

## 📊 Example Results

Based on our testing with the Canadian tech company presentation:
- ✅ Successfully created 13-slide presentation
- ✅ Professional business design
- ✅ Chinese language support
- ✅ Multiple export formats (PDF, PPTX)
- ✅ High-quality AI-generated content

## 🌟 Special Features

### Business-Ready Templates
- Investor pitch decks
- Market entry strategies
- Government reports
- Enterprise presentations

### International Focus
- Multilingual support (60+ languages)
- Cross-cultural business content
- Global market analysis
- International expansion guides

### AI-Powered Content
- Natural language to slides
- Automatic layout and design
- Professional formatting
- Brand-consistent styling

## 🔧 Integration Notes

- API responses are asynchronous - use polling for status
- Generated content appears in Gamma dashboard
- File URLs expire after certain time
- Themes can be customized in Gamma dashboard
- Multiple export formats available

## 🔗 API Integration

**Base URL:** `https://public-api.gamma.app/v1.0`
**Authentication:** API Key (X-API-KEY header)
**Rate Limits:** 250k tokens/minute (free tier)

See `references/gamma_api.md` for complete API documentation.

---

**Ready to create professional presentations with AI!** 🚀