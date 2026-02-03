# Gamma.app API Reference

## Overview

Gamma.app provides a comprehensive API for creating AI-powered presentations, documents, websites, and social media content programmatically.

**Base URL:** `https://public-api.gamma.app/v1.0`

**Authentication:** API Key (X-API-KEY header)

## Key Endpoints

### 1. Generate a Gamma Post
**POST** `/generations`

Create a new gamma (presentation/document) from text input.

**Request Body:**
```json
{
  "inputText": "Your content here",
  "textMode": "generate",
  "format": "presentation",
  "textOptions": {
    "language": "zh",
    "tone": "professional"
  },
  "numCards": 13,
  "cardSplit": "auto",
  "additionalInstructions": "Make it business-appropriate"
}
```

**Response:**
```json
{
  "generationId": "abc123",
  "status": "processing",
  "gammaUrl": "https://gamma.app/g/abc123"
}
```

### 2. Create from Template
**POST** `/create-from-template`

Create using an existing template.

**Request Body:**
```json
{
  "templateId": "template-123",
  "companyName": "Your Company",
  "format": "presentation",
  "textOptions": {
    "language": "zh"
  }
}
```

### 3. Get File URLs
**GET** `/generations/{generationId}/file-urls`

Get download URLs for generated content.

**Response:**
```json
{
  "fileUrls": [
    {
      "url": "https://...",
      "format": "pdf",
      "expiry": "2026-02-03T15:00:00Z"
    }
  ],
  "formats": ["pdf", "pptx"]
}
```

### 4. List Themes
**GET** `/themes`

Get available themes.

**Response:**
```json
{
  "themes": [
    {
      "id": "theme-123",
      "name": "Professional Blue",
      "description": "Clean business theme"
    }
  ]
}
```

## Parameters Explained

### Content Parameters

**inputText** (string, required)
- Text content for generation (1-100,000 characters)
- Can be as little as a few words or pages of text

**textMode** (string, enum)
- "generate" - Generate new content (default)
- "condense" - Condense existing content
- "preserve" - Keep content as-is

**format** (string, enum)
- "presentation" - PowerPoint-style slides
- "document" - Document format
- "webpage" - Web page format
- "social" - Social media format

### Design Parameters

**themeId** (string, optional)
- ID of theme from Gamma
- If not specified, default workspace theme is used

**numCards** (integer, 1-75)
- Number of slides/cards to create
- Default: 10, max: 75 for Ultra users

**cardSplit** (string, enum)
- "auto" - Automatic division (default)
- "inputTextBreaks" - Use input text breaks

### Text Options

**textOptions.language** (string)
- Output language code
- Examples: "en", "zh", "fr", "de", "ja"

**textOptions.tone** (string)
- Content tone: "professional", "casual", "formal", etc.

### Export Options

**exportAs** (string, enum)
- Additional export formats
- "pdf" or "pptx"

## Example Use Cases

### 1. Business Presentation
```json
{
  "inputText": "Chinese tech companies going global to Canada...",
  "format": "presentation",
  "textOptions": {
    "language": "zh",
    "tone": "professional"
  },
  "numCards": 13,
  "exportAs": "pptx"
}
```

### 2. Document Creation
```json
{
  "inputText": "Annual report for ABC Corporation...",
  "format": "document",
  "textOptions": {
    "language": "en",
    "tone": "formal"
  },
  "exportAs": "pdf"
}
```

### 3. Social Media Post
```json
{
  "inputText": "New product launch announcement...",
  "format": "social",
  "textOptions": {
    "language": "en",
    "tone": "engaging"
  }
}
```

## Rate Limits

- **Free Tier:** 250,000 input tokens per minute
- **Pro Tier:** Higher limits available
- **Ultra Tier:** Highest limits available

## Error Codes

- **200** - Success
- **400** - Bad Request
- **401** - Unauthorized (invalid API key)
- **429** - Rate Limited

## Best Practices

1. **Chunk Large Content** - Split very long content into smaller pieces
2. **Use Templates** - Leverage existing templates for consistency
3. **Specify Language** - Always set language for best results
4. **Test Formats** - Try different formats for your use case
5. **Export Options** - Always specify export format needed

## Integration Notes

- API responses are asynchronous - use polling or webhooks for status
- Generated content appears in separate dashboard tab
- File URLs expire after certain time
- Themes can be customized in Gamma dashboard

---

**For OpenClaw Integration:** This API is perfect for creating professional presentations and documents from natural language input, which is exactly what we need for the Chinese tech company presentation!