# HEARTBEAT.md - Hourly Operations Check

Run every hour to maintain operational excellence.

## Tasks

### 1. Check for Incomplete Tasks
- Review any pending work or TODO items
- Send Telegram update if there are outstanding items requiring attention
- Prioritize by urgency and business impact

### 2. Git Repository Maintenance
- Check for uncommitted changes in workspace
- If changes exist:
  - Review and categorize changes by function/purpose
  - Create clear, descriptive commit messages
  - Commit changes in logical groups
  - Push to remote repository
  - Send Telegram notification about what changed

### 3. System Health Check
- Verify all scheduled jobs are running correctly
- Check for any error logs or issues
- Monitor API key status and rate limits

## Execution Guidelines
- **Be concise**: Only notify if action is needed
- **Be proactive**: Fix small issues automatically
- **Be transparent**: Always inform about significant changes
- **Be efficient**: Batch similar operations together

## Output Format
If everything is fine: Silent (no notification)
If action taken: Brief Telegram message with summary of changes
If attention needed: Clear description of the issue and recommended action
