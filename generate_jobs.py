#!/usr/bin/env python3
"""
Generate jobs.html from Excel job order data.
Anonymizes company names with one-sentence business descriptors.
Full JD content extracted from messy HTML cells.
"""

import openpyxl
import re
import html as html_mod
from collections import defaultdict

EXCEL = '/Users/zach.g/.hermes/cache/documents/doc_147198b5f972_joborder 2026-05-18 12_57_18.xlsx'
JOBS_HTML = '/Users/zach.g/dev/zach-website/jobs.html'

# ─── Company anonymization map ───
COMPANY_MASKS = {
    '行吟信息科技（上海）有限公司': '生活方式社区平台',
    '腾讯科技（深圳）有限公司': '互联网科技巨头',
    '上海哔哩哔哩科技有限公司': '视频社区与内容平台',
    '北京达佳互联信息技术有限公司': '短视频与直播平台',
    'Vattention 时空注力': 'AI视频交互创新公司',
    '易点天下网络科技股份有限公司(西安点告网络科技有限公司）': '出海营销科技平台',
    '钛动科技股份有限公司': '出海营销与AI技术平台',
    '北京奇点星宇科技有限公司': '社交产品创新公司',
    '北京翼鸥教育科技有限公司': '在线教育科技平台',
    '北京百易图信息科技有限公司': '协同文档与SaaS工具开发商',
    '杭州当贝网络科技有限公司': '出海AIGC营销平台',
    '杭州帷幄未来科技有限公司': '零售AI与数字化解决方案商',
    '上海国智技术有限公司': '大数据与AI基础设施服务商',
    '深圳枫叶互动科技有限公司': '海外互动内容平台',
    'SCITIX SPACE (SGP) PTE. LTD.': '跨境AI云原生平台',
    'shopee虾皮': '东南亚电商平台',
    '阿斯利康全球研发（中国）有限公司': '全球药企中国研发中心',
    '北京米连科技有限公司': '社交与内容创新平台',
    '礼来 Lilly': '全球医药巨头',
    '南芥智能科技（南京）有限公司': 'AI技术研发公司',
    '深圳九瓴科技有限公司': 'AI Agent技术公司',
    '小满科技': '智能CRM与出海SaaS平台',
    '中国太平洋保险(集团)股份有限公司': '大型保险金融集团',
    '作业帮教育科技（北京）有限公司': 'AI教育科技平台',
    '北京智者天下科技有限公司': '知识问答社区平台',
    '广州智品网络科技有限公司': '移动广告技术公司',
    '杭州容量互娱科技有限公司': '短剧与AI内容制作公司',
    '上海合合信息科技股份有限公司': '智能文档与数据服务商',
    '上海声网科技有限公司': '实时音视频PaaS平台',
    '上海稀宇极智科技有限公司': 'AI大模型创新公司（MiniMax）',
    '深信服科技股份有限公司': '网络安全与云计算服务商',
    '英矽智能科技（上海）有限公司': 'AI制药先锋企业',
    '长量基金': '金融科技与基金销售平台',
    '浙江莲花紫星智算科技有限公司': '智算与AI基础设施运营商',
}


def classify_cat(pos_title):
    """Classify position into one of 7 categories based on title keywords."""
    p = pos_title.lower()
    if any(k in p for k in ['infra', 'gpu', '训练', '推理', '存储', '调度', 'kubernetes', 'devops',
                            '查询分析', 'flink', '实时计算', '压缩算法', '异构计算', 'pytorch',
                            '机器学习优化', '并行文件', 'maas', 'solution architect', '算力',
                            '训练框架', '推理框架', '平台全栈', 'platform', '存储引擎',
                            '分布式存储', '数据分析', '大数据', '引擎研发', '计算引擎',
                            '查询', 'ai infra']):
        return 'infra'
    if any(k in p for k in ['agent', '智能体', 'llm', '大模型', '后训练', '微调', 'sft', 'rlhf',
                            '强化学习', '应用算法', '对话', '评测', 'ai engineer', '语义',
                            'function calling', 'prompt', 'language model', '语言大模型',
                            'codebuddy', 'workbuddy', 'harness', '大模型应用', 'workflow',
                            'workflow', 'agent研发', 'agent评估', '框架']):
        return 'agent'
    if any(k in p for k in ['推荐', '搜索', '广告', '搜广推', '召回', '排序', '算法', '多模态',
                            'nlp', '风控', '机器学习', '数据科学', '数据挖掘', 'aigc', '图像',
                            '视频生成', '音频', '语音', '视频理解', '算法工程师',
                            '算法专家', '算法leader', 'ai算法', '深度学习', 'sparkfly',
                            '推荐系统', 'mac', 'nlp']):
        return 'algo'
    if any(k in p for k in ['多媒体', '音视频', '媒体', 'webgpu', 'webcodecs', '编解码',
                            'ffmpeg', '视频编辑', '渲染', 'opengl', '流式视频', '直播',
                            '视频', '音频', 'web 多媒体']):
        return 'media'
    if any(k in p for k in ['产品', 'pm', 'product', '产品经理', '产品总监', '商业化',
                            '营销云', '投放', '品牌', '流量', '商单', 'adx', 'sparkfly',
                            '产品专家', '技术部负责人', 'cto', '技术总监', '总经理',
                            '制作人', '导演', '制片']):
        return 'product'
    if any(k in p for k in ['增长', 'growth', '出海', '海外', '运营', '优化师', '红人',
                            'kol', 'seo', 'sem', '发行', '商务', 'bd', '市场',
                            '社媒运营', '内容运营', '主编', '用户增长']):
        return 'growth'
    return 'exec'


def clean_html(raw):
    """Strip HTML tags and return clean text lines from JD content."""
    if not raw or str(raw).strip() in ('None', 'null', '', 'nan'):
        return []
    text = str(raw)
    # Remove style blocks
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    # Convert line breaks to newlines
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'</li>', '\n', text)
    text = re.sub(r'</p>', '\n', text)
    text = re.sub(r'</div>', '\n', text)
    text = re.sub(r'</pre>', '\n', text)
    text = re.sub(r'<pre[^>]*>', '', text)
    text = re.sub(r'<ol[^>]*>', '', text)
    text = re.sub(r'</ol>', '', text)
    text = re.sub(r'<ul[^>]*>', '', text)
    text = re.sub(r'</ul>', '', text)
    text = re.sub(r'<li[^>]*>', '• ', text)
    # Remove remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    text = html_mod.unescape(text)
    
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if not line or line in ('&nbsp;', 'null', 'None', '', '•'):
            continue
        # Skip section headers
        skip_headers = ['职位描述', '岗位职责', '任职要求', 'Qualifications', 'qualifications',
                       'Responsibilities', 'responsibilities', 'About the', 'Main Duties',
                       '职位需求', '岗位要求', '工作职责', 'About the Company',
                       '关于我们', '【关于我们】', '【岗位职责】', '【任职要求】']
        if any(line.startswith(h) or line == h for h in skip_headers):
            continue
        # Normalize bullet points
        line = re.sub(r'^\d+[\.\\)、]\s*', '• ', line)
        if not line.startswith('• '):
            line = '• ' + line
        lines.append(line)
    
    # Remove consecutive duplicates
    seen = set()
    unique = []
    for line in lines:
        if line not in seen and len(line) > 5:
            seen.add(line)
            unique.append(line)
    return unique[:25]


def format_items(items):
    """Format cleaned items as <li> HTML."""
    if not items:
        return '<p style="color:#64748b;font-style:italic;">详细JD请私信联系</p>'
    result = []
    for item in items:
        text = item[2:] if item.startswith('• ') else item
        escaped = html_mod.escape(text)
        result.append(f'<li>{escaped}</li>')
    return '\n'.join(result)


def generate_card(idx, pos_title, company, location, jd_items, req_items, cat, salary=''):
    """Generate a single job card HTML."""
    mask = COMPANY_MASKS.get(company, company)
    desc = f"{pos_title} — {mask} · {location}"
    jd_html = format_items(jd_items)
    req_html = format_items(req_items)
    salary_html = f'<span class="job-salary">{html_mod.escape(salary)}</span>' if salary else ''
    
    return f'''<div class="job-card" data-cat="{cat}">
<div class="job-header" onclick="toggleJobCard(this.parentElement)">
<span class="job-id">#{idx:03d}</span>
<h3 class="job-title">{html_mod.escape(pos_title)}</h3>
<span class="job-company-mask">{html_mod.escape(mask)}</span><span class="job-location">📍 {html_mod.escape(location)}</span>{salary_html}
<p class="job-desc">{html_mod.escape(desc)}</p>
<div class="expand-indicator">[ 点击展开查看完整JD ] <span class="arrow">▼</span></div>
</div>
<div class="job-full-details">
<div class="job-detail-section">
<div class="job-detail-label">📌 工作职责</div>
<div class="job-detail-body">{jd_html}</div>
</div>
<div class="job-detail-section">
<div class="job-detail-label">🎯 任职要求</div>
<div class="job-detail-body">{req_html}</div>
</div>
</div>
</div>'''


def main():
    wb = openpyxl.load_workbook(EXCEL)
    ws = wb.active
    
    # Parse all rows
    all_jobs = []
    for r in range(2, ws.max_row + 1):
        pos_title = str(ws.cell(row=r, column=1).value or '').strip()
        company = str(ws.cell(row=r, column=2).value or '').strip()
        jd_raw = ws.cell(row=r, column=3).value
        location = str(ws.cell(row=r, column=4).value or '').strip()
        req_raw = ws.cell(row=r, column=5).value
        salary = str(ws.cell(row=r, column=9).value or '').strip()
        inner_raw = ws.cell(row=r, column=8).value
        
        if not pos_title:
            continue
        
        cat = classify_cat(pos_title)
        jd_items = clean_html(jd_raw)
        req_items = clean_html(req_raw)
        
        # Merge inner content (col 8) into JD if available
        inner_items = clean_html(inner_raw)
        if inner_items:
            # Filter out generic header lines like "Bonus Points", "You might be a fit"
            filtered = [i for i in inner_items if not any(h in i for h in [
                'Bonus Points', 'You might be a fit', '你可能会','加分项'
            ])]
            if filtered:
                jd_items.extend(filtered)
        
        # Also try inner content if JD is empty
        if not jd_items:
            jd_items = inner_items[:]
        if not req_items and jd_items:
            req_items = jd_items[:]
        
        # Clean salary
        if salary in ('None', 'null', '', 'nan'):
            salary = ''
        
        all_jobs.append({
            'title': pos_title,
            'company': company,
            'mask': COMPANY_MASKS.get(company, company),
            'location': location,
            'jd_items': jd_items,
            'req_items': req_items,
            'cat': cat,
            'salary': salary,
        })
    
    print(f"Parsed {len(all_jobs)} positions")
    
    # Group by category
    cats = ['infra', 'agent', 'algo', 'media', 'product', 'growth', 'exec']
    cat_names = {
        'infra': 'AI Infra & 云计算基础设施',
        'agent': 'AI Agent & 大模型应用',
        'algo': '算法、搜广推与多模态',
        'media': '视频/多媒体工程',
        'product': '产品与商业化',
        'growth': '增长、出海与运营',
        'exec': '管理与战略',
    }
    cat_titles = {
        'infra': '01 // AI Infra & 云计算基础设施',
        'agent': '02 // AI Agent & 大模型应用',
        'algo': '03 // 算法、搜广推与多模态',
        'media': '04 // 视频/多媒体工程',
        'product': '05 // 产品与商业化',
        'growth': '06 // 增长、出海与运营',
        'exec': '07 // 管理与战略',
    }
    
    grouped = defaultdict(list)
    for job in all_jobs:
        grouped[job['cat']].append(job)
    
    # Generate category groups
    total = 0
    card_html = ''
    for cat in cats:
        jobs = grouped.get(cat, [])
        if not jobs:
            continue
        total += len(jobs)
        card_html += f'\n<!-- ═══ {cat_titles[cat]} ═══ -->\n'
        card_html += f'<div class="category-group" data-category="{cat}">\n'
        card_html += f'<h2 class="category-title">{cat_titles[cat]}</h2>\n'
        card_html += '<div class="jobs-grid">\n'
        
        for idx, job in enumerate(jobs, 1):
            card_html += generate_card(
                idx, job['title'], job['company'],
                job['location'], job['jd_items'], job['req_items'],
                job['cat'], job['salary']) + '\n'
        
        card_html += '</div>\n</div>\n'
    
    # Generate filter section with correct counts
    c_infra = len(grouped.get('infra', []))
    c_agent = len(grouped.get('agent', []))
    c_algo = len(grouped.get('algo', []))
    c_media = len(grouped.get('media', []))
    c_product = len(grouped.get('product', []))
    c_growth = len(grouped.get('growth', []))
    c_exec = len(grouped.get('exec', []))
    
    filter_html = f'''<div class="kicker">/ LIVE_OPPORTUNITIES</div>
<h1 class="main-title">热招机会 <span style="font-size:0.5em;color:#64748b;font-family:'Space Mono';">({total} 个活跃职位)</span></h1>

<div class="job-category-filters">
<span class="cat-filter active" data-cat="all">🔘 全部 ({total})</span>
<span class="cat-filter" data-cat="infra">AI Infra & 云计算 ({c_infra})</span>
<span class="cat-filter" data-cat="agent">AI Agent & 大模型 ({c_agent})</span>
<span class="cat-filter" data-cat="algo">算法/搜广推/多模态 ({c_algo})</span>
<span class="cat-filter" data-cat="media">视频/多媒体工程 ({c_media})</span>
<span class="cat-filter" data-cat="product">产品与商业化 ({c_product})</span>
<span class="cat-filter" data-cat="growth">增长/出海/运营 ({c_growth})</span>
<span class="cat-filter" data-cat="exec">管理与战略 ({c_exec})</span>
</div>'''
    
    # Build the complete new jobs section
    new_section = f'<!-- ═══ Jobs Content ═══ -->\n<div class="jobs-section">\n{filter_html}\n\n{card_html}</div>\n'
    
    # Read existing jobs.html
    with open(JOBS_HTML, 'r') as f:
        content = f.read()
    
    # Find insertion point
    start_marker = '<!-- ═══ Jobs Content ═══ -->'
    start_idx = content.find(start_marker)
    if start_idx < 0:
        print("ERROR: Could not find Jobs Content marker")
        return
    
    # Find where the jobs section ends - look for the next script tag
    after_section = content.find('<script>', start_idx + 100)
    if after_section < 0:
        print("ERROR: Could not find script tag after jobs section")
        return
    
    # Find the closing </div> of jobs-section before <script>
    end_marker = content.rfind('</div>', start_idx, after_section)
    
    # Rebuild
    output = content[:start_idx] + new_section + content[end_marker + 6:]
    
    with open(JOBS_HTML, 'w') as f:
        f.write(output)
    
    print(f"✅ Generated {total} job cards across {len([c for c in cats if grouped.get(c)])} categories")
    print(f"   Written to {JOBS_HTML}")
    
    # Verify
    verify_count = output.count('class="job-card"')
    print(f"   Verified: {verify_count} job-card elements in output")


if __name__ == '__main__':
    main()
