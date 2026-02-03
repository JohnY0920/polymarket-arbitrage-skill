#!/usr/bin/env python3
"""
Create the Chinese Tech Companies Going Global to Canada presentation
using Gamma.app API

This creates the specific 13-slide presentation you provided.
"""

import json
import sys
import argparse
from pathlib import Path

# Your presentation content (Chinese)
PRESENTATION_CONTENT = """中国科技企业出海加拿大

Slide 1: 封面
标题: 加拿大：中国科技企业全球化的最优跳板
副标题: 为什么越来越多的中国科技公司选择加拿大作为出海第一站
视觉元素: 简洁的世界地图，标注中国→加拿大→全球的路径

Slide 2: 开场 - 一个正在发生的趋势
中国科技企业出海新范式
过去5年，超过200家中国科技公司在加拿大设立实体：
🤖 AI/ML公司：85+
💰 Fintech公司：45+
🏥 Healthtech公司：30+
📱 SaaS平台：40+

为什么是加拿大？
三个关键词：
Trusted - 北约成员国，五眼联盟，天然可信标签
Connected - 三大自贸协定交汇点，一次设立辐射全球
Smart - 全球第6最佳创业生态，AI研究世界前3

"加拿大不是备选方案，而是战略选择"

Slide 3: 全球视角 - 加拿大在哪里？
Startup Genome 2024全球创业生态排名
全球Top 10：
1. 硅谷（美国）
2. 纽约（美国）
3. 伦敦（英国）
4. 洛杉矶（美国）
5. 特拉维夫（以色列）
6. 🍁 加拿大整体
7. 北京（中国）
8. 波士顿（美国）
9. 巴黎（法国）
10. 西雅图（美国）

北美城市排名：
硅谷 #1
纽约 #2
洛杉矶 #4
多伦多-滑铁卢 #15（🍁 北美第4）
波士顿 #8
西雅图 #10

关键洞察：
加拿大是唯一同时具备以下特征的市场：
✅ Top 10全球创业生态
✅ 对中国企业政治友好
✅ 运营成本比美国低40%+
✅ 无缝进入美国和欧洲市场

Slide 4: 核心问题 - 中国企业出海面临什么？
三大战略困境

困境1: 美国 - 政治壁垒
🚫 CFIUS严格审查
🚫 Entity List风险
🚫 品牌信任度：31%（美国消费者）
🚫 政策不确定性极高（随政府更替剧变）

困境2: 新加坡 - "洗白"标签
⚠️ 欧美市场审查加强40%
⚠️ 被标记为"中资洗白地"
⚠️ 需要disclosure ultimate beneficial owner
⚠️ 物理距离远离欧美主流市场

困境3: 直接出口 - 多重劣势
💰 关税壁垒（25-60%）
🏷️ 品牌认知：全球消费者信任度<35%
🔒 数据本地化无法满足
📉 B2B采购中80%欧美企业排除中国供应商

核心挑战：
如何在保持成本优势的同时，获得欧美市场的信任和准入？

Slide 5: 加拿大解决方案 - 三大战略价值
价值1: 可信身份 (Trusted Identity)
品牌溢价效应
消费者信任度对比：
加拿大品牌 中国品牌 差距
美国市场 72% 31% +41%
欧洲市场 68% 28% +40%
日本市场 65% 25% +40%
澳洲市场 70% 30% +40%

实际影响：
"Designed in Canada" vs "Made in China"
进入企业采购shortlist
政府项目feasible（非敏感领域）
Premium pricing可行（+30-50%）

价值2: 全球通达 (Global Access)
一次设立，三大市场
→ 北美（USMCA）
无缝服务美国客户
软件/SaaS零关税
同时区、无语言障碍

→ 欧洲（CETA）
参与欧盟公共采购
服务贸易零关税
数据传输便利（PIPEDA与GDPR对齐）

→ 亚太（CPTPP）
覆盖日本、澳洲、新加坡等11国
数字产品零关税
禁止强制数据本地化

市场覆盖：
人口：15亿+
GDP：$45T+
自贸协定国家：40+

价值3: 智能生态 (Smart Ecosystem)
世界级AI研究
Vector Institute（多伦多）- Geoffrey Hinton
Mila（蒙特利尔）- Yoshua Bengio
Amii（埃德蒙顿）- Rich Sutton
三位图灵奖得主，全球仅此一处

顶尖人才可及
STEM毕业生/年：50,000+
AI研究人员：2,000+
薪资成本：硅谷的55%
移民签证：2周获批（vs 美国H-1B抽签）

研发税收支持
SR&ED：政府返还35%研发支出
每投入$1研发，获得$0.35返还
AI/ML项目几乎都qualify

Slide 6: 数据说话 - 成本与效率
运营成本对比（10人AI团队）
旧金山 多伦多 节省
人员 $1.8M $1.1M 39%
办公 $150K $60K 60%
其他 $280K $200K 29%
小计 $2.23M $1.36M 39%
SR&ED返还 $0 -$150K -
实际成本 $2.23M $1.21M 46%

关键指标：
💰 年节省：$1M+
⏱️ 达到盈亏平衡：快12个月
📈 同样资金支持更长runway
💡 更早实现product-market fit

这意味着：
Bootstrap更容易存活
VC资金使用效率更高
创始人保留更多equity

Slide 7: 地缘政治 - 2026黄金窗口
卡尼政府开启中加合作新时代
政策转向（2026年初）
《中加经贸合作路线图》签署
"政经分离"原则明确
非军事敏感领域全面开放
重启经济财金战略对话
明确欢迎的领域：
✅ 绿色科技与清洁能源
✅ 民用AI与数字医疗
✅ 农业科技与食品安全
✅ 教育科技
明确排除的领域：
❌ 军事技术
❌ 5G网络设备（华为中兴）
❌ 量子计算军事应用

独立于美国的科技政策
加拿大不再简单跟随美国禁令：
领域 美国 加拿大
AI投资审查 有（Outbound screening） 无
人才签证 H-1B抽签（中签率<30%） 2周快速通道
TikTok 考虑全面ban 仅政府设备禁用
数据监控 CLOUD Act PIPEDA保护

这意味着什么：
更稳定的政策环境
更少的政治风险
更多的合作机会

Slide 8: 真实案例 - 他们为什么选择加拿大
案例1: Cohere
背景: 多伦多AI独角兽，估值$2.2B+
为什么在加拿大：
✅ Geoffrey Hinton的学生，leveraging Vector Institute
✅ Enterprise focus（避开与OpenAI的consumer竞争）
✅ "加拿大AI"品牌 = 可信、安全、neutral
结果: 成立3年估值$2B+
全球500+企业客户
多语言能力（100+语言）成为差异化优势

案例2: Wealthsimple
背景: 加拿大Fintech独角兽，估值$5B+
为什么在加拿大：
✅ 监管清晰（vs 美国50州碎片化）
✅ 市场gap（传统银行服务差）
✅ 本土品牌信任度
结果: 300万+用户
2024年实现盈利
向美国扩张时已有solid foundation

案例3: 某中国AI公司（匿名）
背景: 计算机视觉技术，原计划直接进美国
为什么改选加拿大：
🚫 美国CFIUS审查卡住6个月
✅ 转向加拿大，3个月完成设立
✅ 从加拿大服务美国客户，无障碍
结果: 首年营收$2M（80%来自美国客户）
获得加拿大政府SR&ED返还$280K
正在准备进入欧洲市场（leveraging CETA）

Slide 9: 路径清晰 - 如何开始
典型时间轴
Phase 1: 设立（1-3个月）
公司注册
银行开户
团队初建
成本: $30K-50K

Phase 2: 验证（4-9个月）
产品本地化
首批客户
市场反馈
目标: $30K-60K MRR

Phase 3: 扩张（10-18个月）
规模化运营
SOC 2认证
进入美国/欧洲
目标: $100K+ MRR

关键里程碑：
✅ 3个月：完成设立，开始运营
✅ 6个月：首批paying customers
✅ 12个月：达到盈亏平衡
✅ 18个月：考虑Series A（if needed）

与硅谷路径对比：
加拿大：稳健增长，12-18个月盈亏平衡
硅谷：快速burn，24-36个月盈亏平衡

关键差异: 加拿大模式更少依赖外部融资

Slide 10: 谁适合加拿大路径？
强烈推荐：
✅ B2B SaaS & Enterprise Software
加拿大企业市场成熟
SOC 2/PIPEDA compliance是competitive advantage
例如：HR tech, CRM, BI tools, Marketing automation

✅ AI/ML技术驱动的产品
可以leverage Vector/Mila研究生态
SR&ED税收支持研发
例如：Computer vision, NLP, Recommendation engines

✅ Fintech & Healthtech
监管清晰可预测
数据隐私要求严格（反而是优势）
例如：Payment, Insurance, Telemedicine

✅ 需要进入欧美市场的任何科技公司
品牌可信度提升40%
三大自贸协定通达全球
规避直接从中国出口的壁垒

不太适合：
❌ 5G/量子/军事敏感技术
❌ 纯中国市场的产品（无需海外实体）
❌ 硬件制造为主（设计+品牌可以）

Slide 11: 关键数据总结
一张图看懂加拿大优势
维度 数据 含义
创业生态 全球第6 世界级创业环境
成本节省 45% vs 硅谷运营成本
品牌提升 +40% 消费者信任度提升
研发支持 35%返还 SR&ED税收抵免
市场覆盖 15亿人口 三大自贸协定
人才签证 2周 Global Talent Stream
AI排名 前3 研究机构密度
政策稳定 中高 法治框架确定性

核心结论：
加拿大是唯一同时满足以下条件的市场：
世界级创业生态
对中国企业友好
成本可控
全球市场通达

Slide 12: 下一步
我们今天讨论了什么：
✅ 为什么加拿大是战略选择而非备选
✅ 三大核心价值：可信身份、全球通达、智能生态
✅ 2026政治黄金窗口
✅ 真实案例与清晰路径

接下来可以做什么：
Option 1: 深度对话
我们可以：
分析您的具体业务是否适合加拿大
评估市场机会和竞争格局
讨论潜在的挑战和风险
定制初步进入策略

Option 2: 市场调研
我们帮您：
识别target客户群体
分析竞争对手
评估regulatory requirements
估算成本和时间轴

Option 3: 实地考察
如果您计划访问加拿大：
安排与本地企业会面
参观AI研究机构
对接潜在合作伙伴
体验商业环境

今天没有推销，只是分享信息
我们相信informed decision is the best decision
欢迎随时联系继续对话

无论最终是否选择加拿大，我们都希望这次交流有价值

Slide 13: 联系方式
继续对话
📧 Email: [your email]
📞 Phone: [your phone]
🌐 Website: [your website]
💬 WeChat: [your wechat]

或者
扫描二维码：
下载完整白皮书
预约咨询时间
加入我们的邮件列表（每月出海insights）

感谢您的时间

"正确的时间，正确的地点，正确的策略"

2026年，加拿大等待着您的到来""