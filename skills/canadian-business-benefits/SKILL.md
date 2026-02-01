---
name: canadian-business-benefits
description: Help Canadian businesses find and match government benefits, grants, loans, and support programs. Asks qualifying questions about industry, location, business goals, and project details to identify relevant programs from Innovation Canada's database of 1581+ federal, provincial, and municipal benefits. Provides program details, eligibility criteria, and application guidance. Use when user needs Canadian business funding, government grants, startup support, R&D funding, export assistance, or any government business programs.
---

# Canadian Business Benefits Finder

Match Canadian businesses with relevant government benefits, grants, loans, and support programs.

## What This Does

Helps businesses navigate Canada's 1581+ government support programs by:
1. Asking qualifying questions about the business
2. Matching answers to relevant programs
3. Providing program details and eligibility
4. Guiding through application preparation

**Data source:** Innovation Canada (innovation.ised-isde.canada.ca)

## Quick Start

### User Asks About Benefits

**Triggers:**
- "What Canadian business grants are available?"
- "Find me government funding for my startup"
- "I need help finding business benefits in Ontario"
- "Are there R&D grants for tech companies?"

### Workflow

1. **Gather information** through conversational questions
2. **Use browser automation** to query Innovation Canada
3. **Extract and filter** matching programs
4. **Present results** with details
5. **Provide application guidance**

## Conversational Question Flow

### Always Start With Context

Before asking questions, explain:
> "I'll help you find relevant Canadian government benefits. I'll ask a few questions to narrow down the 1581+ available programs to the ones that match your business."

### Question Sequence

Ask questions naturally based on what the user has already shared. Don't ask redundant questions.

#### 1. Type of Support (Critical)

**Ask:** "What type of support are you looking for?"

**Options to suggest:**
- Grants and funding (non-repayable money)
- Loans and capital investments
- Tax credits
- Wage subsidies and interns
- Expert advice and consulting
- Partnering and collaboration opportunities
- Access to researchers and facilities
- Other support

**Multiple selections OK**: User can want both grants AND expert advice

#### 2. Province/Territory (Critical)

**Ask:** "Which province or territory is your business in?"

**Options:**
- All Canadian provinces/territories
- Can select multiple if operating in several locations
- See `references/filters_and_criteria.md` for full list

#### 3. Industry/Sector (Important)

**Ask:** "What industry or sector is your business in?"

**Examples:**
- Technology/IT
- Manufacturing
- Agriculture
- Clean tech/Green energy
- Healthcare
- Professional services
- Retail
- etc.

**Note:** Be flexible with industry names - Innovation Canada has comprehensive industry taxonomy

#### 4. Main Business Goal (Important)

**Ask:** "What's your main goal right now?"

**Common goals:**
- Start or buy a business
- Grow and expand
- Conduct R&D or develop products
- Sell internationally/export
- Hire or train employees
- Buy equipment or property
- Increase working capital
- Improve productivity/efficiency
- Reduce pollution/improve energy efficiency

**Multiple selections OK**

#### 5. Funding Amount (If applicable)

**Ask:** "How much funding are you looking for?"

**Ranges:**
- Up to $50,000
- Up to $250,000
- $20,000 to $500,000
- $500,000 and above
- Not sure / any amount

#### 6. Project Stage (Optional but helpful)

**Ask:** "What stage is your project or business at?"

**Typical stages:**
- Idea/concept
- Planning/research
- Development
- Pilot/testing
- Commercialization
- Growth/scaling

#### 7. Additional Context (Optional)

- Company size (employees, revenue)
- Specific project details
- Timeline/urgency
- Past funding received

### Handling Partial Information

**If user provides some info upfront:**
- Don't re-ask what they've told you
- Fill in known criteria
- Ask only for missing critical info

**Example:**
User: "I need R&D grants for my tech startup in Ontario"

✅ Already know:
- Support type: grants
- Goal: R&D
- Industry: tech
- Province: Ontario

✅ Still need:
- Funding amount
- Project stage
- Specific project area

## Using Browser Automation

Once you have enough information (minimum: support type, province), use browser to find matches:

### Browser Workflow

1. **Start browser:**
   ```
   browser action=start profile=clawd
   ```

2. **Navigate to Innovation Canada:**
   ```
   browser action=open targetUrl="https://innovation.ised-isde.canada.ca/" profile=clawd
   ```

3. **Click English:**
   - Take snapshot
   - Click "English" button

4. **Fill questionnaire:**
   - Step 1: Select support type, amount, goals
   - Step 2: Select province, industry
   - Click "Next" or "See your results"

5. **Extract results:**
   - Take snapshot of results page
   - Extract program names, descriptions, amounts
   - Get links to detailed pages

6. **Present to user:**
   - Format results clearly
   - Include: program name, type, amount, eligibility summary
   - Provide links for details

See `references/filters_and_criteria.md` for exact filter options and element references.

## Presenting Results

### Format

Present results in an organized, scannable format:

```
🎯 Found [X] matching programs for your business:

**1. [Program Name]**
- **Type:** Grant / Loan / Tax Credit / etc.
- **Amount:** Up to $X or percentage
- **Eligibility:** Key requirements
- **Deadline:** If applicable
- **Link:** [URL]

**2. [Program Name]**
...

**Top Recommendations:**
Based on your [industry/goal/location], I'd prioritize:
1. [Program] - because [reason]
2. [Program] - because [reason]
```

### Prioritization

Help user focus on best matches:
- **Best fit:** Programs closely matching all criteria
- **Quick wins:** Easy to apply, high approval rate
- **High value:** Largest funding amounts
- **Time-sensitive:** Programs with approaching deadlines

## Application Guidance

### After Presenting Results

Offer to help with next steps:
> "Would you like help preparing to apply for any of these programs?"

### Common Application Requirements

**Most programs need:**
1. **Business information**
   - Incorporation details
   - Business number (BN)
   - Financial statements

2. **Project details**
   - Detailed project plan
   - Budget and timeline
   - Expected outcomes/impact

3. **Eligibility proof**
   - Province/sector confirmation
   - Size requirements (employees, revenue)
   - Years in operation

4. **Supporting documents**
   - Market research
   - Letters of support
   - Quotes for equipment/services

### Preparation Checklist

Generate a custom checklist based on selected programs:

```
**Application Preparation for [Program Name]:**

☐ **Before you start:**
   - Verify eligibility criteria
   - Review application deadline
   - Read program guidelines fully

☐ **Documents to gather:**
   - [List specific to program]

☐ **Information to prepare:**
   - [List specific requirements]

☐ **Questions to answer:**
   - [Common application questions]

☐ **Tips for this program:**
   - [Program-specific advice]
```

## Common Scenarios

### Startup Seeking Initial Funding

**Typical profile:**
- Support: grants and funding
- Goal: start a business
- Amount: up to $50,000
- Stage: idea or planning

**Likely matches:**
- Provincial startup grants
- Federal IRAP (if tech/innovation)
- Regional development programs
- Youth/newcomer programs (if applicable)

### Growing Business Needing Capital

**Typical profile:**
- Support: loans and capital investments
- Goal: grow and expand
- Amount: $500,000+
- Stage: commercialization/growth

**Likely matches:**
- BDC loans and financing
- Export Development Canada (if exporting)
- Industry-specific growth funds
- Provincial venture programs

### R&D / Innovation Project

**Typical profile:**
- Support: grants, researchers/facilities
- Goal: conduct R&D, develop products
- Amount: varies widely
- Stage: development

**Likely matches:**
- IRAP (Industrial Research Assistance Program)
- SR&ED tax credits
- Mitacs (if partnering with universities)
- NRC programs
- Provincial innovation funds

### Export / International Expansion

**Typical profile:**
- Support: grants, expert advice
- Goal: sell internationally
- Selling internationally: planning or active
- Amount: varies

**Likely matches:**
- CanExport programs
- Trade Commissioner Service
- Export Development Canada
- Provincial trade missions

## Important Notes

### Eligibility Varies

- **Size limits:** Many programs have employee/revenue caps
- **Sector restrictions:** Some programs target specific industries
- **Location requirements:** Provincial programs require business presence
- **Stage requirements:** Some only for startups, others only for established businesses

### Application Timing

- **Rolling intake:** Apply anytime (most common)
- **Specific deadlines:** Mark calendars, don't miss windows
- **Multi-stage:** Some programs have pre-qualification rounds
- **Processing time:** Can take weeks to months for decisions

### Matching Funds

Many programs require:
- Co-investment from business
- Percentage split (e.g., government 50%, business 50%)
- In-kind contributions may count
- Other funding sources may be required

### Restrictions

Common restrictions:
- Cannot be used for certain expenses (e.g., land purchase)
- May require hiring criteria (Canadian citizens/PRs)
- Intellectual property considerations
- Reporting and compliance obligations

## Troubleshooting

### "Too many results"

**Response:** Narrow criteria
- Add more filters (industry, specific goal, amount)
- Focus on highest priority needs
- Consider project stage

### "No results found"

**Response:** Broaden criteria
- Try "all support" instead of specific type
- Select "all of Canada" for province
- Check if selections are too restrictive
- May need to adjust industry categorization

### "Programs don't match my needs"

**Response:** Refine understanding
- Ask more about specific needs
- Explore alternative support types
- Consider non-financial support (advice, connections)
- Check if user qualifies (size, sector, stage)

## Resources

- **Innovation Canada:** https://innovation.ised-isde.canada.ca/
- **Canada Business:** https://www.canada.ca/en/services/business.html
- **BDC (Bank Development Canada):** https://www.bdc.ca/
- **Export Development Canada:** https://www.edc.ca/
- **IRAP (Industrial Research Assistance Program):** https://nrc.canada.ca/en/support-technology-innovation/nrc-irap

## References

See `references/filters_and_criteria.md` for:
- Complete filter options
- Question structure
- Province/territory list
- Industry categories
- Amount ranges
- Goal options

## Success Metrics

Good outcomes:
- User finds 3-10 relevant programs (not too many, not too few)
- At least 1-2 programs are highly relevant
- User understands eligibility and next steps
- Application preparation guidance is actionable

## Follow-up

After initial search:
- Offer to search with different criteria
- Provide application help for specific programs
- Set reminders for application deadlines
- Check back on application progress

---

**Remember:** This skill helps Canadian businesses access government support. Be thorough in understanding their needs, and prioritize programs that genuinely match their situation.
