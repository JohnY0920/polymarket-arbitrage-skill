# Canadian Business Benefits Finder

A Clawdbot/OpenClaw skill to help Canadian businesses find and match government benefits, grants, loans, and support programs.

## 🇨🇦 What This Does

Helps businesses navigate **1581+ government programs** from Innovation Canada by:
- Asking smart qualifying questions
- Matching businesses to relevant programs
- Providing program details and eligibility
- Guiding through application preparation

**Data Source:** [Innovation Canada](https://innovation.ised-isde.canada.ca/)

## 🚀 Quick Start

### Installation (for Clawdbot users)

```bash
clawdbot skills install https://github.com/JohnY0920/canadian-business-benefits-skill/raw/master/canadian-business-benefits.skill
```

### Usage

Simply ask:
- "Find me Canadian business grants"
- "What government funding is available for my tech startup in Ontario?"
- "I need help finding R&D grants"

The skill will guide you through questions and find matching programs.

## 🎯 Features

### Intelligent Questioning
- Asks only relevant questions based on context
- Adapts based on what you've already shared
- Handles partial information gracefully

### Comprehensive Coverage
- **1581+ programs** from federal, provincial, and municipal levels
- All types of support: grants, loans, tax credits, advice, partnerships
- All provinces and territories
- All industries and sectors

### Detailed Results
For each matching program:
- Program name and type
- Funding amount or support offered
- Eligibility requirements
- Application deadlines (if applicable)
- Direct links to program details

### Application Guidance
- Common requirements across programs
- Document checklists
- Eligibility verification
- Tips to strengthen applications
- What to expect after submission

## 📋 Question Categories

The skill asks about:

1. **Type of Support**
   - Grants, loans, tax credits, wage subsidies
   - Expert advice, partnerships, research access

2. **Business Location**
   - Province/Territory
   - Can select multiple locations

3. **Industry/Sector**
   - Technology, manufacturing, agriculture, clean tech, etc.
   - Comprehensive industry taxonomy

4. **Business Goals**
   - Start/grow business, R&D, export, hire, improve efficiency, etc.
   - Can select multiple goals

5. **Funding Amount** (if applicable)
   - Up to $50K, $250K, $500K, $500K+

6. **Project Stage** (optional)
   - Idea, planning, development, commercialization, growth

## 🛠️ Components

### SKILL.md
Main skill instructions including:
- Conversational question flow
- Browser automation workflow
- Result presentation format
- Application preparation guidance

### references/filters_and_criteria.md
Complete filter reference:
- All filter options and categories
- Question structure
- Province/territory list
- Industry categories

### references/application_guide.md
Comprehensive application guide:
- General requirements
- Project-specific requirements
- Supporting documents
- Eligibility verification
- Application tips and common mistakes
- Post-submission process

### scripts/find_benefits.py
Placeholder for future automation

## 📖 Example Scenarios

### Startup Seeking Initial Funding
**Input:**
- Support: grants
- Province: Ontario
- Industry: Technology
- Goal: start a business
- Amount: up to $50K

**Result:** Provincial startup grants, IRAP, regional development programs

### R&D Project
**Input:**
- Support: grants, researchers
- Province: British Columbia
- Industry: Clean tech
- Goal: conduct R&D
- Amount: $500K+

**Result:** IRAP, SR&ED tax credits, Mitacs, NRC programs, provincial innovation funds

### Export Expansion
**Input:**
- Support: grants, expert advice
- Province: Quebec
- Goal: sell internationally
- Amount: varies

**Result:** CanExport programs, Trade Commissioner Service, EDC, provincial trade missions

## ⚠️ Important Notes

- **Eligibility varies** - Size limits, sector restrictions, location requirements
- **Application timing** - Some programs always open, others have specific deadlines
- **Matching funds** - Many programs require co-investment
- **Restrictions apply** - Check each program's specific requirements

## 🔗 Resources

- **Innovation Canada:** https://innovation.ised-isde.canada.ca/
- **Canada Business:** https://www.canada.ca/en/services/business.html
- **BDC:** https://www.bdc.ca/
- **Export Development Canada:** https://www.edc.ca/
- **IRAP:** https://nrc.canada.ca/en/support-technology-innovation/nrc-irap

## 📚 Documentation

Full documentation available in:
- `skills/canadian-business-benefits/SKILL.md` - Complete skill guide
- `references/filters_and_criteria.md` - Filter options
- `references/application_guide.md` - Application preparation

## ⚖️ License

MIT License - See LICENSE file

## 🤝 Contributing

Contributions welcome! This skill helps Canadian businesses access government support.

## 📧 Contact

- **GitHub:** [@JohnY0920](https://github.com/JohnY0920)
- **Issues:** https://github.com/JohnY0920/canadian-business-benefits-skill/issues

---

Built by JoJo (AI assistant) for John Yin  
Version: 1.0  
Date: February 2026
