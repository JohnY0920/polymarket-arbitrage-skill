#!/usr/bin/env python3
"""
Polymarket Daily Report Email Sender
Sends daily Polymarket trends and opportunities report via email
"""

import os
import sys
import json
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def run_poly_command(command):
    """Run poly CLI command and return output"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"❌ Command failed: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ Command execution failed: {str(e)}")
        return None

def get_top_markets():
    """Get top markets by volume"""
    output = run_poly_command("poly markets --limit 10")
    if not output:
        return None
    
    # Parse the output - handle new rich table format with line wrapping
    markets = []
    lines = output.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for market data lines (start with │ but not header lines)
        if line.startswith('│') and not any(header in line for header in ['Question', 'Prices', 'Volume', '━━━']):
            parts = [p.strip() for p in line.split('│') if p.strip()]
            
            if len(parts) >= 3:
                question = parts[0]
                prices = parts[1]
                volume = parts[2]
                
                # Check if question is complete (no ... at the end)
                if not question.endswith('...'):
                    # Complete question, add to markets
                    markets.append({
                        'question': question,
                        'prices': prices,
                        'volume': volume
                    })
                else:
                    # Incomplete question, collect continuation lines
                    full_question = question
                    
                    # Look for continuation lines (they start with │ and have the rest of the question)
                    j = i + 1
                    while j < len(lines) and lines[j].strip().startswith('│'):
                        cont_line = lines[j].strip()
                        cont_parts = [p.strip() for p in cont_line.split('│') if p.strip()]
                        
                        # If this line has the continuation of our question
                        if len(cont_parts) >= 1 and not cont_parts[0].startswith('Yes:') and not cont_parts[0].startswith('No:'):
                            # This is continuation text
                            continuation = cont_parts[0]
                            full_question = full_question.rstrip('.') + ' ' + continuation
                            
                            # Check if we now have prices and volume on this line
                            if len(cont_parts) >= 3 and 'Yes:' in cont_parts[1]:
                                # Complete market found
                                markets.append({
                                    'question': full_question,
                                    'prices': cont_parts[1],
                                    'volume': cont_parts[2]
                                })
                                break
                        else:
                            # This line has prices/volume, meaning our question is complete
                            if len(cont_parts) >= 2:
                                markets.append({
                                    'question': full_question,
                                    'prices': cont_parts[0],
                                    'volume': cont_parts[1]
                                })
                                break
                            break
                        j += 1
                    i = j - 1  # Skip the lines we already processed
        
        i += 1
    
    return markets

def get_user_balance():
    """Get user balance"""
    output = run_poly_command("poly balance")
    if output:
        return output
    return "Unknown"

def get_user_positions():
    """Get user positions"""
    output = run_poly_command("poly positions")
    if output:
        return output
    return "No positions found"

def format_market_analysis(markets):
    """Format market analysis"""
    analysis = []
    
    for i, market in enumerate(markets[:5], 1):
        # Reconstruct full question based on context and common patterns
        question = market['question']
        
        # Add context based on keywords
        if 'Frank Donovan' in question and 'Venezuela' in question:
            question = 'Will Frank Donovan be the leader of Venezuela by end of 2026?'
        elif 'Judy Shelton' in question and 'Fed' in question:
            question = 'Will Trump nominate Judy Shelton as the next Fed chair?'
        elif 'Bitcoin' in question and '150,000' in question:
            question = 'Will Bitcoin reach $150,000 in February 2026?'
        elif 'Fed' in question and 'interest rates' in question:
            question = 'Will the Fed decrease interest rates by 50+ bps after next meeting?'
        elif 'Kevin Warsh' in question:
            question = 'Will Trump nominate Kevin Warsh as the next Fed chair?'
        elif 'Scott Bessent' in question:
            question = 'Will Trump nominate Scott Bessent as the next Fed chair?'
        elif 'Elon Musk' in question and 'tweets' in question:
            question = 'Will Elon Musk post specified number of tweets this month?'
        elif 'Russia' in question and 'nuclear' in question:
            question = 'Will Russia test a nuclear weapon by specified date?'
        elif 'US strikes Iran' in question:
            question = market['question']  # These seem complete
        
        analysis.append(f"""
### {i}. {question}
**价格:** {market['prices']}
**24小时交易量:** {market['volume']}

**简要分析:**
- 市场流动性: {'高' if 'M' in market['volume'] else '中等' if 'K' in market['volume'] else '低'}
- 建议关注: {'是' if 'M' in market['volume'] else '谨慎关注'}
""")
    
    return '\n'.join(analysis)

def format_html_content(content):
    """Format content for HTML email"""
    html_content = content.replace('\n', '<br>')
    html_content = html_content.replace('**', '<strong>').replace('**', '</strong>')
    html_content = html_content.replace('*', '<em>').replace('*', '</em>')
    
    # Convert numbered lists
    for i in range(1, 6):
        html_content = html_content.replace(f'{i}.', f'<strong>{i}.</strong>')
    
    return f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 700px; margin: 0 auto; }}
            .header {{ background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ padding: 30px; background-color: #ffffff; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            .section {{ margin-bottom: 30px; }}
            .market-item {{ margin-bottom: 25px; padding: 20px; border-left: 4px solid #4ecdc4; background-color: #f8f9fa; border-radius: 8px; }}
            .market-name {{ font-size: 16px; font-weight: bold; color: #495057; margin-bottom: 10px; }}
            .market-stats {{ color: #6c757d; font-size: 14px; margin: 8px 0; }}
            .balance-box {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0; }}
            .positions-box {{ background-color: #e3f2fd; padding: 20px; border-radius: 10px; margin: 20px 0; }}
            strong {{ color: #495057; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎰 Polymarket Daily Report</h1>
            <p>{datetime.now().strftime("%B %d, %Y")}</p>
        </div>
        <div class="content">
            {html_content}
        </div>
    </body>
    </html>
    """

def send_email(subject, html_content, recipients):
    """Send email via SMTP"""
    gmail_email = os.getenv('GMAIL_EMAIL')
    gmail_password = os.getenv('GMAIL_SMTP_PASSWORD')
    
    if not gmail_email or not gmail_password:
        print("❌ Email credentials not found in environment variables")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = gmail_email
        msg['To'] = ', '.join(recipients) if isinstance(recipients, list) else recipients
        
        # Add HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Connect to Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_email, gmail_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(gmail_email, recipients, text)
        server.quit()
        
        print(f"✅ Email sent successfully to {recipients}")
        return True
        
    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")
        return False

def main():
    """Main function"""
    print(f"🎰 Starting Polymarket Daily Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get market data
    markets = get_top_markets()
    if not markets:
        print("❌ Could not fetch market data")
        return False
    
    # Get user info
    balance = get_user_balance()
    positions = get_user_positions()
    
    # Format content
    content = f"""
# 🎰 Polymarket Daily Report
**日期:** {datetime.now().strftime('%Y年%m月%d日')}

## 💰 账户概览
- **当前余额:** {balance}
- **持仓情况:** {positions}

## 🔥 热门市场 (按交易量排序)
{format_market_analysis(markets)}

## 📊 市场洞察
1. **高流动性市场** - 建议优先关注交易量超过$1M的市场
2. **价格发现** - 市场价格反映了集体智慧，但可能存在信息不对称机会
3. **风险管理** - 建议单笔投注不超过总资金的5%

## ⚠️ 风险提示
- 预测市场存在风险，请理性投注
- 市场赔率会实时变动，请及时关注
- 投注前请仔细阅读市场规则

## 🔗 访问Polymarket
前往 [polymarket.com](https://polymarket.com) 查看更多市场机会
"""
    
    # Format HTML content
    html_content = format_html_content(content)
    
    # Get recipients from environment
    recipients_str = os.getenv('RECIPIENT_EMAIL', '')
    if not recipients_str:
        print("❌ No recipients found in RECIPIENT_EMAIL")
        return False
    
    recipients = [email.strip() for email in recipients_str.split(',')]
    
    # Send email
    subject = f"🎰 Polymarket Daily Report - {datetime.now().strftime('%B %d, %Y')}"
    success = send_email(subject, html_content, recipients)
    
    if success:
        print("✅ Polymarket daily report email completed successfully!")
    else:
        print("❌ Polymarket daily report email failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)