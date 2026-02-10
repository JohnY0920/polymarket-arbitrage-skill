# Slack Tunnel Setup Guide

## Current Status
✅ Slack bot token configured in OpenClaw
⚠️ Need public URL for Slack events

## Problem
Your OpenClaw runs locally (localhost:18789). Slack needs a public URL to send events.

## Solution Options

### Option 1: ngrok (Recommended)
```bash
# Install ngrok
curl -s https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-amd64.tgz | tar -xz
mv ngrok /usr/local/bin/

# Start tunnel
ngrok http 18789

# You'll get: https://abc123.ngrok.io
```

### Option 2: LocalTunnel (Alternative)
```bash
# Install localtunnel
npm install -g localtunnel

# Start tunnel
lt --port 18789

# You'll get: https://xyz.loca.lt
```

### Option 3: Cloud Tunnel (Free)
1. **Sign up at**: https://ngrok.com/
2. **Download**: https://ngrok.com/download
3. **Connect your account**: `ngrok authtoken YOUR_TOKEN`
4. **Start tunnel**: `ngrok http 18789`

## Step-by-Step Setup

**1. Choose and install a tunnel service**

**2. Start the tunnel:**
```bash
# For ngrok (after installing)
ngrok http 18789

# Output will be like:
# Forwarding: https://abc123.ngrok.io -> http://localhost:18789
```

**3. Copy the public URL**

**4. Configure Slack Event Subscriptions:**
1. Go to https://api.slack.com/apps
2. Find your "Jojo OpenClaw" app
3. Go to "Event Subscriptions"
4. Turn on "Enable Events"
5. Add URL: `https://abc123.ngrok.io/slack/events`
6. Subscribe to events:
   - `message.channels` (messages in channels)
   - `message.im` (direct messages)
   - `app_mention` (when bot is mentioned)
7. Click "Save Changes"
8. Click "Reinstall to Workspace"

**5. Test the connection:**
- Send DM to @Jojo: "Hello"
- Mention in channel: @Jojo Hello

## Troubleshooting
If messages aren't received:
1. **Check tunnel is running**: `curl http://localhost:4040/api/tunnels`
2. **Verify Slack app**: Check Event Subscriptions URL
3. **Reinstall app**: After URL changes
4. **Check logs**: Look for errors in ngrok output

## Next Steps
Once you have your tunnel URL, let me know and I'll help you configure the Slack Event Subscriptions!