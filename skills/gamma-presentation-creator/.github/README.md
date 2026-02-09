# Gamma Presentation Creator for OpenClaw/Clawdbot

Create professional presentations and documents using Gamma.app's AI-powered API.

## 🚀 Quick Start

This is an **OpenClaw/Clawdbot skill** that integrates Gamma.app's API for AI-powered presentation creation.

### Prerequisites
- OpenClaw/Clawdbot installation
- Gamma.app account with API key
- Python 3.7+

### Installation
1. Clone this repo into your OpenClaw skills directory
2. Configure your Gamma API key
3. Start creating presentations!

## 📋 Features

- ✅ **Text-to-Presentation** - Convert ideas to professional slides
- ✅ **Multiple Formats** - Presentations, documents, webpages, social media
- ✅ **Multilingual Support** - 60+ languages including Chinese, English
- ✅ **Professional Themes** - Business-ready designs
- ✅ **Export Options** - PDF, PPTX, direct sharing
- ✅ **Template Integration** - Use professional templates
- ✅ **CLI Access** - Command-line interface
- ✅ **Programmatic API** - Python integration

## 🎯 Example: Chinese Tech Company Presentation

The skill includes a complete 13-slide presentation about Chinese tech companies expanding to Canada:

**Title:** 加拿大：中国科技企业全球化的最优跳板
**Content:** Market analysis, cost savings (46% vs Silicon Valley), geopolitical insights, real case studies

## 🔧 Configuration

Edit `scripts/gamma_creator.py` and add your API key:
```python
def _get_api_key(self):
    return "YOUR_GAMMA_API_KEY_HERE"
```

## 📝 Usage in OpenClaw

```
"Create a Gamma presentation about [topic]"
"Make a pitch deck for [company]"
"Convert this to slides: [your text]"
```

## 📊 API Integration

**Base URL:** `https://public-api.gamma.app/v1.0`
**Authentication:** X-API-KEY header
**Rate Limits:** 250k tokens/minute (free tier)

## 🛠️ Files Structure

```
gamma-presentation-creator/
├── SKILL.md                                    # Skill documentation
├── README.md                                   # This file
├── GETTING_STARTED.md                          # Setup guide
├── TEST_REPORT.md                              # Testing results
├── scripts/
│   ├── gamma_creator.py                        # Main API integration
│   └── chinese_tech_canada_presentation.py     # Example content
└── references/
    └── gamma_api.md                            # API documentation
```

## 🌟 Built for OpenClaw/Clawdbot

This skill is designed to integrate seamlessly with the OpenClaw/Clawdbot ecosystem for AI-powered automation and presentation creation.

## 📄 License

Part of OpenClaw/Clawdbot skill ecosystem. See LICENSE for details.

---

**Ready to create professional presentations with AI!** 🎯