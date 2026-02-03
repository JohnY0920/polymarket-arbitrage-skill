# Getting Started with Gamma Presentation Creator

## Step 1: Get Your Gamma API Key

1. Visit **https://gamma.app**
2. Sign up or log in
3. Navigate to **Settings → API**
4. Click **"Generate API Key"**
5. Copy your API key

## Step 2: Configure API Key

Edit `scripts/gamma_creator.py` and replace the placeholder:

```python
def _get_api_key(self):
    return "YOUR_GAMMA_API_KEY_HERE"  # ← Put your key here
```

Or set environment variable:
```bash
export GAMMA_API_KEY="your-actual-key-here"
```

## Step 3: Test with Chinese Tech Company Presentation

### Option A: Use the prepared content

```bash
cd /Users/Phoestia/clawd/skills/gamma-presentation-creator

# Load the content from the script
python3 -c "
from scripts.chinese_tech_canada_presentation import PRESENTATION_CONTENT
from scripts.gamma_creator import GammaPresentationCreator

creator = GammaPresentationCreator()
result = creator.create_presentation(
    input_text=PRESENTATION_CONTENT,
    title='加拿大：中国科技企业全球化的最优跳板',
    format='presentation',
    num_cards=13,
    language='zh'
)
print(result)
"
```

### Option B: Quick CLI test

```bash
python3 scripts/gamma_creator.py \
  --input "加拿大：中国科技企业全球化的最优跳板。为什么越来越多的中国科技公司选择加拿大作为出海第一站..." \
  --title "中国科技企业出海加拿大" \
  --format presentation \
  --language zh \
  --num-cards 13
```

## Step 4: Check Results

The API will return:
```json
{
  "success": true,
  "generation_id": "abc123...",
  "status": "processing",
  "url": "https://gamma.app/g/abc123...",
  "message": "Presentation created successfully"
}
```

Visit the URL in your browser to see the generated presentation!

## Step 5: Download Files

Once generation is complete, get download URLs:

```bash
python3 scripts/gamma_creator.py --get-urls "your-generation-id"
```

This returns PDF and PPTX download links.

## Common Issues

### Issue: "401 Unauthorized"
**Solution:** Check your API key is correct

### Issue: "429 Rate Limited"
**Solution:** Wait a minute, you've hit the free tier limit

### Issue: "Missing API key"
**Solution:** Make sure you configured the key in step 2

## What's Next?

- Try different formats: `document`, `webpage`, `social`
- Experiment with themes: Use `--list-themes` first
- Test other languages: `--language en`, `--language fr`, etc.
- Export options: Add `--export-as pdf` or `--export-as pptx`

## Full Chinese Tech Company Presentation

The complete 13-slide presentation content is in:
```
scripts/chinese_tech_canada_presentation.py
```

It includes:
- Cover slide with title and subtitle
- 11 content slides with data, case studies, insights
- Contact information slide

**Content highlights:**
- 200+ Chinese tech companies in Canada
- 46% cost savings vs Silicon Valley
- Access to 3 major trade agreements (USMCA, CETA, CPTPP)
- Real cases: Cohere ($2.2B), Wealthsimple ($5B)
- Clear roadmap: 12-18 months to profitability

## Support

- **Skill docs:** See SKILL.md
- **API reference:** See references/gamma_api.md
- **Gamma support:** https://developers.gamma.app/docs/get-help

---

**Ready to create your first presentation!** 🎯
