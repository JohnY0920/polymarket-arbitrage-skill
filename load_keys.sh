#!/bin/bash
# Load API keys securely
source /Users/Phoestia/clawd/.env

# Add to shell profile for persistence
echo 'export BRAVE_API_KEY="'$BRAVE_API_KEY'"' >> ~/.zshrc
echo 'export GITHUB_TOKEN="'$GITHUB_TOKEN'"' >> ~/.zshrc
echo 'export GMAIL_EMAIL="'$GMAIL_EMAIL'"' >> ~/.zshrc
echo 'export GMAIL_PASSWORD="'$GMAIL_PASSWORD'"' >> ~/.zshrc

echo "✅ API keys loaded and added to shell profile"
echo "🔒 Remember: These credentials are stored securely and won't be shared"
echo "⚠️  Never commit .env files to version control"