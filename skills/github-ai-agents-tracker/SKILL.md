---
name: github-ai-agents-tracker
description: Daily tracker for top growing AI agent repositories on GitHub. Monitors trending autonomous agents, LLM frameworks, and multi-agent systems. Delivers formatted list via Telegram or email.
---

# 🤖 GitHub AI Agents Tracker

Track the top growing AI agent repositories on GitHub daily.

## What It Does

Searches GitHub for trending repositories related to:
- AI agents and autonomous agents
- LLM agent frameworks
- Multi-agent systems
- Agent orchestration tools
- AI automation frameworks

Delivers a daily list of the top 10-20 repositories with:
- Repository name and description
- Star count and growth
- Fork count
- Programming language
- Topics/tags
- Last update date
- Direct GitHub links

## Features

- **Smart Search**: Multiple keyword queries to catch all relevant repos
- **Deduplication**: Removes duplicate repos from different searches
- **Sorted by Stars**: Shows most popular projects first
- **Multiple Formats**: JSON, Markdown, and Telegram-formatted output
- **Rate Limit Aware**: Handles GitHub API limits gracefully
- **Daily Automation**: Can be scheduled via cron

## Quick Start

```bash
cd /Users/Phoestia/clawd/skills/github-ai-agents-tracker/scripts
python3 fetch_trending_agents.py
```

## Output Formats

### Telegram Format (Top 10)
```
🤖 *Top Growing AI Agent Repos*
📅 Feb 05, 2026

*1. microsoft/autogen*
⭐ 25,432 stars | 🍴 3,211 forks
Enable Next-Gen Large Language Model Applications...
🔗 https://github.com/microsoft/autogen
```

### Markdown Format (Top 20)
Full report with descriptions, topics, and update dates

### JSON Format
Complete data for programmatic access

## Daily Automation

### Via OpenClaw Cron
```bash
openclaw cron add \
  --name "GitHub AI Agents Daily" \
  --schedule "0 9 * * *" \
  --timezone "America/Toronto" \
  --command "cd /Users/Phoestia/clawd/skills/github-ai-agents-tracker/scripts && python3 fetch_trending_agents.py"
```

### Via System Cron
```bash
# 9:00 AM daily
0 9 * * * cd /path/to/scripts && python3 fetch_trending_agents.py
```

## Configuration

### GitHub Token (Optional but Recommended)
Without token: 60 requests/hour
With token: 5,000 requests/hour

```bash
export GITHUB_TOKEN=your_github_token
```

Get token at: https://github.com/settings/tokens

### Search Parameters
Edit `fetch_trending_agents.py`:
```python
repos = tracker.search_trending_repos(
    days_back=30,    # Look back 30 days
    min_stars=50     # Minimum 50 stars
)
```

## Keywords Tracked

- "AI agent"
- "autonomous agent"  
- "LLM agent"
- "agent framework"
- "multi-agent"
- "AI automation"

## Requirements

```bash
pip install requests
```

## Usage Examples

### Basic Run
```bash
python3 fetch_trending_agents.py
```

### With GitHub Token
```bash
GITHUB_TOKEN=your_token python3 fetch_trending_agents.py
```

### Send to Telegram
```python
from fetch_trending_agents import GitHubAgentTracker

tracker = GitHubAgentTracker()
repos = tracker.search_trending_repos()
telegram_msg = tracker.format_telegram(repos)

# Send via OpenClaw message tool
# message(action="send", channel="telegram", to="user_id", message=telegram_msg)
```

## Output Files

- `ai_agents_YYYYMMDD.json` - JSON data
- `ai_agents_YYYYMMDD.md` - Markdown report

## Customization

### Add More Keywords
Edit the `queries` list in `search_trending_repos()`:
```python
queries = [
    "AI agent",
    "autonomous agent",
    "your custom keyword"
]
```

### Change Filters
```python
params = {
    "q": f"{query} language:Python pushed:>{date_threshold} stars:>{min_stars}",
    "sort": "stars",  # or "updated", "forks"
    "order": "desc",
    "per_page": 10
}
```

## Integration with Other Skills

### Send via Email (with executive-news-digest)
```python
# Append to daily news digest
```

### Post to Discord/Slack
```python
# Use message tool with appropriate channel
```

### Save to Notion/Obsidian
```python
# Format and save to knowledge base
```

## Notes

- GitHub API has rate limits (60/hour without token, 5000/hour with token)
- Search is limited to Python repos by default (easily customizable)
- Results are cached in JSON files
- Handles API errors gracefully with fallback

## Troubleshooting

### Rate Limit Hit
```
⚠️ Rate limit hit for query: AI agent
```
**Solution:** Add GitHub token or wait 1 hour

### No Results Found
**Solution:** Adjust `min_stars` or `days_back` parameters

---

**Stay updated on the latest AI agent developments!** 🚀
