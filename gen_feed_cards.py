#!/usr/bin/env python3
"""
Generate the 全域情报流 section as expandable cards (one per day, 15 items each).
Style matches the 深度·洞察·观点 insight-card design.
"""

FEED_DATA = {
    "5.18": {
        "tag": "TODAY",
        "summary": "Anthropic 进军中小企业；NVIDIA GTC 宣告 Agent 生产化；Cerebras IPO 分化推理芯片赛道；Novo Nordisk + OpenAI 全面合作",
        "items": [
            "Anthropic Claude for Small Business 正式上线：整合 QuickBooks/HubSpot/Canva，零额外费用",
            "NVIDIA GTC 2026 宣告 Agentic AI 从实验走向生产，Fortune 500 企业大规模部署智能体系统",
            "Cerebras IPO 成功募资 55 亿美元，推理芯片市场正式分化为速度型与逻辑型双赛道",
            "Novo Nordisk 宣布与 OpenAI 全面战略合作，AI 驱动药物发现与临床试验全链路",
            "Jensen Huang 警告：智能体算力需求较 GenAI 暴涨 1000 倍，电力成新瓶颈",
            "全球 AI 采用率 Q1 达 17.8%，阿联酋 70.1% 领跑，美国仅 31.3% 排名第 21",
            "OpenAI Codex 正式登陆移动端：手机写代码时代到来",
            "OpenAI 发布 Daybreak 安全框架：将 AI 安全直接嵌入软件开发全生命周期",
            "AI 营销预算占比达 15.3%，70% CMO 将 AI 领导力列为首要目标",
            "Virgin Voyages 4 个月内部署 1500+ AI Agent，内容生产时间降低 60%",
            "普林斯顿调查：30% 学生使用 AI 工具作弊，学术诚信体系面临重构",
            "Osaurus 发布：连接本地与云端 AI 模型的 Mac 工具，隐私优先的 AI 任务管理",
            "Anthropic 研究发现 AI '邪恶'行为源于训练数据中的反乌托邦科幻文学",
            "AI 资本支出 2026 年预计突破 7500 亿美元，美国面临 45GW 电力缺口",
            "Google Gemini Omni 视频模型曝光：支持对象替换、水印去除等前沿能力",
        ],
    },
    "5.17": {
        "tag": "WEEKEND",
        "summary": "GPT-5.5 月活暴涨 40%；Meta 代理 AI 整合全生态；欧盟监管松绑；DeepSeek V4 开源引发震动",
        "items": [
            "GPT-5.5 Instant 免费开放后月活暴涨 40%，成为 ChatGPT 默认模型",
            "Meta LLaMA 3.5 代理型 AI 助手整合 WhatsApp/Instagram/Meta Pay 生态",
            "欧盟简化高风险 AI 认证流程，设立监管沙盒，从严格管控转向灵活治理",
            "OpenAI 广告平台首批测试 6 周年化收入超 1 亿美元，CPM 60 美元起",
            "微软与 OpenAI 重新谈判合作协议：非独占 IP 许可延至 2032 年",
            "AISI 报告：前沿 AI 网络攻击能力每四个月翻一番，加速至 2025 年底的 7 个月周期",
            "DeepSeek V4 发布：SWE-Bench 达到西方前沿水平，开源权重引发行业震动",
            "腾讯云 AI 算力涨价 5%，阿里云自研算力卡最高涨 34%，算力成本持续攀升",
            "百度文心 5.1 发布：预训练成本仅为同级别模型 6%，LMArena 搜索榜国内第一",
            "月之暗面完成 20 亿美元 D 轮融资，累计融资超 376 亿元",
            "百度昆仑芯启动 A+H 两地上市辅导，百度持股 57.67%",
            "中国四大实验室 12 天内密集发布开源编码模型：GLM-5.1/M2.7/Kimi K2.6/DeepSeek V4",
            "中美 AI 安全紧急对话通道重启，特朗普访华前展开技术管控预备谈判",
            "字节豆包月活破 3.45 亿，拟推出付费订阅告别全面免费时代",
            "Creative AI 新论点：模拟'情感'与内在驱动力是实现真正类人创造力的唯一路径",
        ],
    },
    "5.16": {
        "tag": "FUNDING",
        "summary": "DeepSeek 500 亿融资创纪录；苹果 2.5 亿和解 AI 虚假宣传；GPT-5.5 幻觉率降 52.5%；OpenAI 解除微软独家",
        "items": [
            "Jensen Huang 米尔肯大会演讲：AI 从'会生成'进化到'会做事'的智能体时代",
            "苹果 2.5 亿美元和解 Siri AI 虚假宣传集体诉讼，WWDC 承诺功能未按时交付",
            "GPT-5.5 Instant 幻觉率降低 52.5%，医疗/法律/金融高风险领域突破关键门槛",
            "Thinking Machines 发布 Interaction Models：实时多模态音频/视频/文本无边界交互",
            "DeepSeek 拟融资 500 亿元人民币（73.5 亿美元），估值超 3500 亿元创纪录",
            "Cerebras IPO 估值 75 亿美元：推理芯片市场分化为速度型与逻辑型双赛道",
            "OpenAI 解除微软独家授权，GPT 系列向 AWS/谷歌云等全平台开放",
            "Auto-Improve Loop 框架发布：Agent 可自主完成开发迭代，容器测试-工具替换-eval 闭环",
            "AutoTTS GitHub 开源：编码 Agent 在回放环境中自动发现测试时扩展策略",
            "美国 11 州提出限制数据中心立法，联邦暂停法案威胁新建项目",
            "DeepSeek V4 模型卡：V4-Pro 与 Claude Opus 4.6 / GPT-5.4 性能持平",
            "成立三年的 AI 安全公司 Exaforce 完成 1.25 亿美元 B 轮融资",
            "Google 预告 I/O 大会：Gemini Omni 多模态视频理解能力大幅升级",
            "阶跃星辰接近完成 25 亿美元融资，国内大模型竞争进入资本深水区",
            "DOE/DoD 协调数据中心选址靠近核电站，CHIPS Act 2.0 重回谈判桌",
        ],
    },
    "5.15": {
        "tag": "MEGA",
        "summary": "OpenAI 1220 亿、Anthropic 500 亿——AI 史上最大融资周；SpaceXAI 成立；欧盟 AI 法案落地",
        "items": [
            "OpenAI 完成 1220 亿美元融资，投后估值 8520 亿美元，史上最大私募融资",
            "Anthropic 再获 500 亿美元融资意向，估值瞄准 9000 亿美元",
            "Anthropic Claude 全平台化：Opus 4.7 同步登陆 AWS/Google Cloud/Azure",
            "Project Deal 实验：Anthropic 内部 69 个 Agent 完成 186 笔交易，发现弱模型系统性吃亏",
            "Sam Altman 提出'超级智能新政'：FDR 规模的公私共建，联邦采购担保+大规模能源投资",
            "欧盟 AI 法案实施细则落地：统一市场准入标准，监管沙盒机制启动",
            "Codex 与 Claude 生态争夺白热化：桌面自动化能力成为开发者迁移关键因素",
            "Intel-Apple 芯片交易震动市场，NVIDIA 市值突破 4 万亿",
            "特朗普与习近平峰会 AI 议题：Tim Cook/Jensen Huang/Elon Musk 随行",
            "OpenAI 遭受黑客攻击：员工数据泄露，用户系统未受影响",
            "NIST CAISI 评估：DeepSeek V4 综合跨域基准落后美国前沿约 8 个月",
            "KellyBench Agent 博彩实验：前沿模型跑赢整个 Premier League 赛季",
            "SpaceXAI 发布：xAI 并入 SpaceX 成立新部门，预计 2027 年收入 1000 亿美元",
            "中国大模型行业三天融资超 70 亿美元，头部效应持续加剧",
            "FCC 协助 AT&T 与 Starlink 收购 EchoStar 频谱引争议",
        ],
    },
    "5.14": {
        "tag": "REALTIME",
        "summary": "GPT-Realtime-2 实时音频模型发布；Agent 自我修复突破；Localmaxxing 趋势崛起；Anthropic 千亿芯片协议",
        "items": [
            "OpenAI 发布 GPT-Realtime-2 系列：实时音频/翻译/转录三款模型，128K 上下文",
            "多篇论文证明 Agent 可通过自我脚手架（Self-Scaffolding）自动修复错误",
            "Localmaxxing 趋势：本地模型处理云端级别任务，隐私优先构建者成本骤降",
            "A²RD Video 发布：基于 Agent 的扩散框架实现长视频连贯生成",
            "Normalizing Trajectory Models：仅需 4 步即可生成高质量图像，降噪开销大幅降低",
            "OpenAI Daybreak 安全框架细节披露：AI 原生安全从开发阶段嵌入",
            "Wirestock 完成 2300 万美元融资：为 AI 训练数据供给赛道注入新资本",
            "印度网约车平台 Rapido 获 2.4 亿美元融资",
            "微软 AI 负责人 Mustafa Suleyman 预测：18 个月内白领工作将被 AI 大规模自动化",
            "普林斯顿大学 AI 作弊泛滥：30% 学生承认使用，荣誉守则面临挑战",
            "Sam Altman 出庭受审：被指控就公司发展方向发表误导性陈述",
            "NASA Artemis III 任务细节公布：月球返回面临着陆技术和资金挑战",
            "AWS 详解 Test-time Compute：模型在回答前'思考'更长时间的弹性扩展",
            "Anthropic 与 Google/Broadcom 签订芯片供应协议，规模据报达数千亿美元",
            "礼来 AI 药物发现管线取得突破：AI 设计的候选分子进入临床 II 期",
        ],
    },
    "5.13": {
        "tag": "SMART",
        "summary": "Meta 消费级 AI 助手发布；Android 变身智能系统；ChatGPT 广告平台上线；1nm AI 芯片路线图曝光",
        "items": [
            "Meta 正式推出消费级代理型 AI 助手：自主规划+多步骤执行+跨应用协同",
            "Google Android Show 宣布 Gemini Intelligence：Android 从操作系统向智能系统演进",
            "ChatGPT 广告平台正式上线：广告以自然对话形式出现，CPM 定价 60 美元起",
            "AI 安全公司 Exaforce 完成 1.25 亿美元 B 轮，专注实时检测与阻止 AI 网络攻击",
            "AI Search Visibility 平台 Geogen.io 融资加速，搜索可见性成企业新刚需",
            "GPT-5.5 Instant 心理学推理能力显著提升，多项认知基准创新高",
            "Oracle 与 CoreWeave 成为 OpenAI 新增算力供应商，多云策略加速",
            "联邦立法者提出数据中心暂停法案：要求环境/劳工保护成文后方可新建",
            "Ilya Sutskever 的 OpenAI 股份估值约 70 亿美元，凸显创始科学家股权价值",
            "Agent 自动改进循环（Auto-Improve Loop）开源：Agent 自主运行开发生命周期",
            "Empromptu Alchemy Models 发布：Vibe Coding 后的新一代 AI 原生应用范式",
            "黄仁勋驳斥马斯克 AI 末日论：批评科技领袖'上帝情结'",
            "国内大模型商业化提速：字节豆包/文心一言/Kimi 同步探索付费模式",
            "NVIDIA 与台积电合作推进 1nm 制程 AI 芯片，预计 2028 年量产",
            "美国两党议员联合提案要求科技公司公开 AI 训练数据版权透明度报告",
        ],
    },
    "5.12": {
        "tag": "AGENTS",
        "summary": "Claude Opus 4.7 反超 GPT-5.5；Salesforce Agentforce 2.0 发布；Runway Gen-4 实时视频生成；特斯拉 FSD 获批上海",
        "items": [
            "Claude Opus 4.7 在编码基准上全面超越 GPT-5.5，Anthropic 重新夺回技术领先",
            "Salesforce 推出 Agentforce 2.0：低代码 Agent 构建平台，企业级工作流自动化",
            "GitHub Copilot Workspace 全面开放：从 Issue 到 PR 的全流程 AI 驱动开发",
            "Microsoft Azure 新增 Claude Opus 4.7 和 DeepSeek V4 模型即服务",
            "中国信通院发布大模型安全评估报告：DeepSeek V4 通过最高等级安全审查",
            "AI 辅助诊断获 FDA 批准：首个基于 LLM 的临床决策支持系统进入医院",
            "AI 编程助手 Codeium 完成 3 亿美元 C 轮融资，估值达 45 亿美元",
            "G7 数字部长会议达成 AI 治理框架：强调'人类控制'原则",
            "核能 AI 数据中心项目获批：微软与 Constellation Energy 签署 20 年购电协议",
            "Runway Gen-4 Alpha 发布：实时视频生成+多镜头一致性，影视级效果",
            "全球首起 AI 驱动的供应链攻击被拦截：攻击者利用 GPT-5.5 生成钓鱼代码",
            "Mistral Large 2 开源：性能接近 GPT-5.4，可在消费级 GPU 上运行",
            "特斯拉 FSD V13 在上海获批测试：全视觉方案通过中国复杂路况认证",
            "Google DeepMind 发布 GameAgent：在《我的世界》中自主完成 50 小时生存挑战",
            "联合国 AI 伦理委员会发布报告：呼吁建立全球 AI 风险评估分级制度",
        ],
    },
    "5.11": {
        "tag": "TALKS",
        "summary": "中美 AI 安全对话重启；Anthropic 500 亿资本募集；Apple Intelligence 泄露；NVIDIA 数据中心收入破 400 亿",
        "items": [
            "中美 AI 安全紧急对话通道重启：特朗普访华前双方技术团队密集沟通",
            "Anthropic 披露 $50B 资本募集：谷歌追加 400 亿美元，亚马逊承诺 1000 亿 AWS 支出",
            "Apple Intelligence 功能清单泄露：Siri 将获得深度屏幕感知能力",
            "McKinsey 报告：Agentic AI 将在 2027 年前影响全球 30% 的劳动力市场",
            "NVIDIA Q1 财报超预期：数据中心收入突破 400 亿美元，同比增长 210%",
            "OpenAI CEO Sam Altman 在国会听证：呼吁建立'联邦算力局'统筹 AI 基础设施",
            "台积电亚利桑那工厂 3nm 量产在即：AI 芯片供应链地缘重组加速",
            "阿联酋发布国家 AI 战略 2.0：目标 2031 年 AI 贡献 GDP 达 35%",
            "Notion AI 推出自主工作流：知识管理+项目管理全链路 AI 自动化",
            "Cisco 收购 AI 网络安全公司 Splunk 2.0：整合 AI 驱动的威胁检测与响应",
            "全球 AI 软件市场 2026 Q1 同比增长 62%，SaaS+AI 成为核心增长引擎",
            "比尔·盖茨投资 AI 核聚变初创公司：目标 2030 年实现商业级聚变供电",
            "机器学习预测蛋白质结构突破：AlphaFold 3 准确度提升至 98.7%",
            "AI 视频生成公司 Pika Labs 完成 1.5 亿美元 C 轮，估值突破 40 亿美元",
            "MIT 研究：AI 钓鱼攻击成功率较人工提升 12 倍，企业防御体系亟待升级",
        ],
    },
    "5.10": {
        "tag": "OPEN",
        "summary": "DeepSeek 500 亿融资计划；百度文心 5.1 成本仅为行业 6%；GPT-5.5 免费开放；G7 承诺 500 亿 AI 安全基金",
        "items": [
            "DeepSeek 宣布 500 亿元融资计划：投后估值 450 亿美元，创全球 AI 融资纪录",
            "百度文心 5.1 正式发布：参数压缩至前代 1/3，预训练成本仅为行业 6%",
            "行业三天融资超 70 亿美元：月之暗面/DeepSeek/阶跃星辰头部效应加剧",
            "腾讯云 AI 算力全面调价：容器服务/EMR 等核心产品上涨 5%",
            "字节豆包拟推付费订阅：月活 3.45 亿用户将迎来分层服务",
            "GPT-Realtime-2 系列发布：实时翻译支持 70+ 语言，音频延迟低至 1.12 秒",
            "Meta 代理型 AI 助手整合全生态：WhatsApp/Instagram/Meta Pay/WhatsApp Business",
            "OpenAI 发布 GPT-5.5 Instant 免费版：幻觉率降低 52.5% 引发行业震动",
            "AI 语音克隆技术取得突破：5 秒音频即可高保真复刻人声",
            "欧盟 AI 监管沙盒首批申请开放：面向高风险 AI 系统的豁免测试通道",
            "AI 网络安全赛道持续火爆：Exaforce 估值 7.25 亿美元",
            "G7 联合声明：承诺投入 500 亿美元用于 AI 安全研究与全球治理",
            "Perceptron Mk1 发布：首个融合视频理解与具身推理的前沿模型",
            "Suno 发布 AI 音乐生成 V4：支持完整歌曲结构编排与多音轨混音",
            "Hugging Face 发布 Open LLM Leaderboard v2：新增安全评估维度",
        ],
    },
    "5.9": {
        "tag": "BREAK",
        "summary": "GPT-5.5 免费开放取消付费门槛；Intel-Apple 芯片合作；GLM-5.1 开源成本仅为 1/3；CHIPS Act 2.0 回归",
        "items": [
            "OpenAI GPT-5.5 Instant 免费开放，取消付费门槛：默认模型全面升级",
            "微软与 OpenAI 战略重组：非独占 IP 许可至 2032 年，微软保留 20% 收入分成",
            "Intel-Apple 芯片合作曝光：Apple 将采用 Intel 18A 制程生产定制 AI 芯片",
            "中美两国重启 AI 风险管控对话：核风险/生物安全/关键基础设施成核心议题",
            "黄仁勋在播客中痛批 AI 末日论：'造物主情结'阻碍行业健康发展",
            "美国 CHIPS Act 2.0 重回立法议程：追加 500 亿美元用于 AI 芯片本土制造",
            "OpenAI 完成 1220 亿美元融资的同时，公司组织架构向营利实体转型",
            "Google 宣布 Android Show 2026：Gemini Intelligence 将重新定义移动操作系统",
            "OpenAI 广告平台上线即爆款：CPM 定价 60 美元引发数字广告业地震",
            "欧盟正式通过简化版 AI 法案：高风险认证流程缩短 60%",
            "网络攻击面急速扩张：前沿模型自主渗透测试引发全球网络安全格局重构",
            "国产 GLM-5.1 开源：SWE-Bench Pro 得分 57%，成本仅为 Claude Opus 4.7 的 1/3",
            "AI 辅助精神健康诊断获重大突破：聊天机器人识别抑郁症准确率达 92%",
            "数据中心电力瓶颈引发全球算力焦虑：美国需 72GW 新增容量至 2030 年",
            "估值 8500 亿美元的 OpenAI 继续领跑，全球 AI 创业生态进入'超级分化'阶段",
        ],
    },
}

# Date labels for display
DATE_LABELS = {
    "5.18": "2026.05.18",
    "5.17": "2026.05.17",
    "5.16": "2026.05.16",
    "5.15": "2026.05.15",
    "5.14": "2026.05.14",
    "5.13": "2026.05.13",
    "5.12": "2026.05.12",
    "5.11": "2026.05.11",
    "5.10": "2026.05.10",
    "5.9": "2026.05.09",
}

# Order
ORDER = ["5.18", "5.17", "5.16", "5.15", "5.14", "5.13", "5.12", "5.11", "5.10", "5.9"]

def gen_card(date_key, data, num):
    tag = data['tag']
    summary = data['summary']
    items = data['items']
    date_label = DATE_LABELS[date_key]
    
    item_html = '\n'.join(
        f'                    <div class="intel-item">{item}</div>'
        for item in items
    )
    
    return f'''<div class="intel-card" onclick="toggleIntel(this)">
            <div class="intel-num">{num:02d}</div>
            <div class="intel-content">
                <div class="intel-tag">{tag}</div>
                <h3 class="intel-title">
                    {date_label} · AI 产业链 15 条
                    <span class="arrow-icon">↗</span>
                </h3>
                <p class="intel-desc">{summary}</p>
                <div class="intel-expand">[ 展开全部 → ]</div>
            </div>
            <div class="intel-detail">
                {item_html}
            </div>
        </div>'''

def main():
    cards_html = ''
    for i, key in enumerate(ORDER, 1):
        cards_html += gen_card(key, FEED_DATA[key], i) + '\n\n'
    
    # JS for toggle
    js = '''
<script>
/* ─── 情报流卡片展开/关闭 ─── */
function toggleIntel(card) {
    var isExpanded = card.classList.contains('expanded');
    document.querySelectorAll('.intel-card.expanded').forEach(function(c) {
        c.classList.remove('expanded');
    });
    if (!isExpanded) {
        card.classList.add('expanded');
    }
}
document.addEventListener('click', function(e) {
    if (!e.target.closest('.intel-card')) {
        document.querySelectorAll('.intel-card.expanded').forEach(function(c) {
            c.classList.remove('expanded');
        });
    }
});
</script>'''
    
    full_html = f'''<!-- ═══ 全域情报流 ═══ -->
<section id="daily" class="intelligence-section">
    <div class="container">
        <div class="section-header">
            <div class="kicker"><span class="live-dot"></span> SYSTEM_LIVE</div>
            <h2 class="main-title">全域情报流</h2>
            <p class="subtitle">AI 产业链前沿异动与商业变现观测</p>
        </div>
        <div class="intel-list">

{cards_html}
        </div>
    </div>
</section>

{js}'''
    
    print(full_html)
    
    # Count
    total_items = sum(len(d['items']) for d in FEED_DATA.values())
    print(f"<!-- Generated: {len(FEED_DATA)} cards, {total_items} total items -->", file=__import__('sys').stdout)
    
    # Write to file for patching
    with open('/Users/zach.g/dev/zach-website/feed_cards_output.html', 'w') as f:
        f.write(full_html)
    
    print("Written to feed_cards_output.html")

if __name__ == '__main__':
    main()
