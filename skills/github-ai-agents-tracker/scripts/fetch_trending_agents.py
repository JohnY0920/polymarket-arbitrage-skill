#!/usr/bin/env python3
"""
GitHub AI Agents Tracker
Fetches top growing AI agent repositories daily
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict

class GitHubAgentTracker:
    def __init__(self, github_token=None):
        self.github_token = github_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if github_token:
            self.headers["Authorization"] = f"token {github_token}"
    
    def search_trending_repos(self, days_back=7, min_stars=50) -> List[Dict]:
        """Search for trending AI agent repositories"""
        # Calculate date for search (repos created/updated in last N days)
        date_threshold = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        
        # AI agent related keywords
        queries = [
            "AI agent",
            "autonomous agent",
            "LLM agent",
            "agent framework",
            "multi-agent",
            "AI automation"
        ]
        
        all_repos = []
        
        for query in queries:
            # GitHub search API
            search_url = f"{self.base_url}/search/repositories"
            params = {
                "q": f"{query} language:Python pushed:>{date_threshold} stars:>{min_stars}",
                "sort": "stars",
                "order": "desc",
                "per_page": 10
            }
            
            try:
                response = requests.get(search_url, headers=self.headers, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    items = data.get("items", [])
                    
                    for repo in items:
                        repo_info = {
                            "name": repo.get("full_name"),
                            "description": repo.get("description", "No description"),
                            "stars": repo.get("stargazers_count", 0),
                            "forks": repo.get("forks_count", 0),
                            "language": repo.get("language", "Unknown"),
                            "url": repo.get("html_url"),
                            "created_at": repo.get("created_at"),
                            "updated_at": repo.get("updated_at"),
                            "topics": repo.get("topics", []),
                            "query": query
                        }
                        all_repos.append(repo_info)
                elif response.status_code == 403:
                    print(f"⚠️ Rate limit hit for query: {query}")
                else:
                    print(f"Error searching for '{query}': {response.status_code}")
            except Exception as e:
                print(f"Error fetching repos for '{query}': {e}")
        
        # Remove duplicates by repo name
        unique_repos = {}
        for repo in all_repos:
            name = repo["name"]
            if name not in unique_repos:
                unique_repos[name] = repo
            elif repo["stars"] > unique_repos[name]["stars"]:
                unique_repos[name] = repo
        
        # Sort by stars descending
        sorted_repos = sorted(unique_repos.values(), key=lambda x: x["stars"], reverse=True)
        
        return sorted_repos[:20]  # Top 20
    
    def format_markdown(self, repos: List[Dict]) -> str:
        """Format repositories as markdown"""
        output = []
        output.append(f"# 🤖 Top Growing AI Agent Repositories")
        output.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n")
        output.append(f"**Total Found:** {len(repos)} repositories\n")
        output.append("---\n")
        
        for i, repo in enumerate(repos, 1):
            output.append(f"## {i}. [{repo['name']}]({repo['url']})")
            output.append(f"⭐ **Stars:** {repo['stars']:,} | 🍴 **Forks:** {repo['forks']:,} | 💻 **Language:** {repo['language']}")
            output.append(f"\n**Description:** {repo['description']}\n")
            
            if repo.get('topics'):
                topics_str = ", ".join([f"`{t}`" for t in repo['topics'][:5]])
                output.append(f"**Topics:** {topics_str}\n")
            
            output.append(f"**Last Updated:** {repo['updated_at'][:10]}\n")
            output.append("---\n")
        
        return "\n".join(output)
    
    def format_telegram(self, repos: List[Dict]) -> str:
        """Format repositories for Telegram"""
        output = []
        output.append(f"🤖 *Top Growing AI Agent Repos*")
        output.append(f"📅 {datetime.now().strftime('%b %d, %Y')}\n")
        
        for i, repo in enumerate(repos[:10], 1):  # Top 10 for Telegram
            name = repo['name'].replace('_', '\\_')
            desc = repo['description'][:100] + "..." if len(repo['description']) > 100 else repo['description']
            desc = desc.replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace('`', '\\`')
            
            output.append(f"*{i}. {name}*")
            output.append(f"⭐ {repo['stars']:,} stars | 🍴 {repo['forks']:,} forks")
            output.append(f"{desc}")
            output.append(f"🔗 {repo['url']}\n")
        
        return "\n".join(output)
    
    def save_results(self, repos: List[Dict], format="json"):
        """Save results to file"""
        timestamp = datetime.now().strftime("%Y%m%d")
        
        if format == "json":
            filename = f"ai_agents_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(repos, f, indent=2)
            print(f"✅ Saved to {filename}")
        
        elif format == "markdown":
            filename = f"ai_agents_{timestamp}.md"
            md_content = self.format_markdown(repos)
            with open(filename, 'w') as f:
                f.write(md_content)
            print(f"✅ Saved to {filename}")
        
        return filename

def main():
    """Main entry point"""
    import os
    
    # Get GitHub token from environment (optional but recommended)
    github_token = os.environ.get('GITHUB_TOKEN')
    
    if not github_token:
        print("⚠️ No GITHUB_TOKEN found. API rate limit will be lower (60 req/hour vs 5000).")
        print("   Set GITHUB_TOKEN env var for higher limits.\n")
    
    tracker = GitHubAgentTracker(github_token)
    
    print("🔍 Searching for trending AI agent repositories...")
    repos = tracker.search_trending_repos(days_back=30, min_stars=50)
    
    if repos:
        print(f"✅ Found {len(repos)} repositories\n")
        
        # Save as JSON
        tracker.save_results(repos, format="json")
        
        # Save as Markdown
        tracker.save_results(repos, format="markdown")
        
        # Print Telegram format
        print("\n📱 Telegram Format:")
        print("=" * 60)
        print(tracker.format_telegram(repos))
    else:
        print("❌ No repositories found")

if __name__ == "__main__":
    main()
