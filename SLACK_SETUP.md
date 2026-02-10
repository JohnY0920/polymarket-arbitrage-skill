# Slack Setup Guide for Jojo

## Current Status
✅ Slack configuration framework added to OpenClaw
⚠️ Need to add bot token (provided separately)

## Configuration Setup

1. **Add Bot Token**
   ```bash
   # Add to your .env file:
   export SLACK_BOT_TOKEN="your-bot-token-here"
   ```

2. **Slack App Requirements**
   Create a Slack app at https://api.slack.com/apps with these scopes:
   - `chat:write` - Send messages
   - `chat:write.public` - Send to public channels  
   - `channels:history` - Read channel history
   - `channels:read` - Read channel info
   - `groups:history` - Read private channels
   - `im:history` - Read direct messages
   - `mpim:history` - Read multi-party messages

3. **Install App**
   - Install to your workspace
   - Copy the Bot User OAuth Token
   - Add it to your environment variables

4. **Test Connection**
   - Invite @Jojo to your Slack workspace
   - Mention me: @Jojo
   - Test group chat functionality

## Security Notes
- Keep bot token secure and private
- Use environment variables for tokens
- Never commit actual tokens to git
- GitHub push protection will prevent token commits

Configuration location: /Users/Phoestia/clawd/config/slack.json (template)
