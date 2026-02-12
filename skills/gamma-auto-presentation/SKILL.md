# Gamma Auto Presentation Skill

Automatically generate presentations using Gamma.app API from research topics and email them to recipients.

## Overview

This skill connects to Gamma.app's API to automatically create professional presentations from research topics, research data, or prompts. It can generate various types of presentations and automatically email them to specified recipients.

## Features

- ✅ **Automatic Presentation Generation** - Create presentations from research topics
- ✅ **Multiple Formats** - Support for presentations, documents, and websites
- ✅ **Customizable Themes** - Professional, creative, and other themes
- ✅ **Email Integration** - Automatically send presentations via email
- ✅ **Research Data Processing** - Convert research into structured presentations
- ✅ **CLI Interface** - Easy command-line usage
- ✅ **Batch Processing** - Handle multiple topics/research data

## Installation

```bash
# Ensure Gamma API key is set
export GAMMA_API_KEY="sk-gamma-hClm0HmnAKp1Mo8oM1POPPVqPvJdbH4PJiOrxN8JzTk"

# Set email credentials
export GMAIL_EMAIL="your-email@gmail.com"
export GMAIL_SMTP_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="recipient1@example.com,recipient2@example.com"
```

## Usage

### Basic Presentation Generation

```bash
# Generate from a topic
cd /Users/Phoestia/clawd/skills/gamma-auto-presentation/scripts
python3 gamma_auto_presentation.py "AI Agents in 2024"

# Generate with research data
python3 gamma_auto_presentation.py "AI Agents in 2024" "Recent developments in autonomous AI agents include..." "user@example.com"
```

### Advanced Usage

```bash
# Generate with custom theme and language
python3 gamma_auto_presentation.py \
  "Quantum Computing Applications" \
  "Quantum computing is revolutionizing..." \
  "researcher@university.edu,professor@university.edu" \
  --theme creative \
  --language en \
  --format presentation
```

## API Reference

### GammaAutoPresentation Class

```python
from gamma_auto_presentation import GammaAutoPresentation

generator = GammaAutoPresentation()

# Create presentation from topic
result = generator.create_presentation(
    topic="Your Topic",
    content="Research content here",
    presentation_type="presentation",
    theme="professional"
)

# Generate from research
result = generator.generate_from_research(
    research_topic="AI Trends",
    research_data="Your research data here"
)

# Send via email
generator.send_email(result, ["recipient@example.com"])
```

## Configuration

### Environment Variables

- `GAMMA_API_KEY` - Your Gamma.app API key
- `GAMMA_API_BASE` - API base URL (default: https://api.gamma.app/v1)
- `GMAIL_EMAIL` - Gmail address for sending emails
- `GMAIL_SMTP_PASSWORD` - Gmail app password
- `RECIPIENT_EMAIL` - Default recipients (comma-separated)

### Presentation Options

- **Type**: `presentation`, `document`, `website`
- **Theme**: `professional`, `creative`, `minimal`, `bold`
- **Language**: `en`, `zh`, `es`, `fr`, etc.

## Output

The skill generates:
- JSON result with presentation metadata
- Public URL to view the presentation
- Email notification with presentation link
- Local JSON backup of the result

## Error Handling

The skill handles common errors:
- API connectivity issues
- Invalid API keys
- Email sending failures
- Missing environment variables

## Examples

### Research Presentation
```bash
python3 gamma_auto_presentation.py \
  "Climate Change Impact on Agriculture" \
  "Recent studies show that rising temperatures are affecting crop yields globally..." \
  "climate@research.org,farmer@coop.com"
```

### Business Presentation
```bash
python3 gamma_auto_presentation.py \
  "Q4 2024 Market Analysis" \
  "Our market research indicates strong growth in..." \
  "ceo@company.com,board@company.com" \
  --theme professional
```

## Troubleshooting

### Common Issues

1. **API Key Invalid**
   - Ensure your Gamma API key is correct
   - Check if key has necessary permissions

2. **Email Sending Failed**
   - Verify Gmail app password is correct
   - Check if 2FA is enabled on Gmail account

3. **No Presentations Found**
   - Check your research data format
   - Ensure topic is specific enough

### Debug Mode
Run with verbose output:
```bash
python3 gamma_auto_presentation.py "Topic" 2>&1 | tee debug.log
```

## Security Notes

- Store API keys securely (use environment variables)
- Use app-specific passwords for Gmail
- The skill handles secrets safely in .env files
- GitHub push protection prevents accidental commits of secrets