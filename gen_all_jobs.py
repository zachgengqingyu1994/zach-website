#!/usr/bin/env python3
"""Generate complete jobs.html with all 200 cards + full JD content from Excel"""

import openpyxl
import re
import html as html_mod

wb = openpyxl.load_workbook('/Users/zach.g/.hermes/cache/documents/doc_9863893dc942_joborder 2026-05-17 17_12_02.xlsx')
ws = wb['Sheet1']

company_masks = {
    'SCITIX SPACE (SGP) PTE. LTD.': '跨境AI云原生平台',
    'shopee虾皮': '东南亚电商平台',
    'Vattention 时空注力': 'AI视频创作平台',
    '阿斯利康全球研发（中国）有限公司': '跨国药企研发中心',
    '北京百易图信息科技有限公司': 'AI文档与白板协作平台',
    '北京米连科技有限公司': '社交与AI创新平台',
    '北京奇点星宇科技有限公司': '出海短视频内容平台',
    '北京翼鸥教育科技有限公司': '在线教育科技公司',
    '北京智者天下科技有限公司': '知识问答社区',
    '广州智品网络科技有限公司': '出海广告优化平台',
    '杭州当贝网络科技有限公司': '出海营销AIGC平台',
    '杭州容量互娱科技有限公司': 'AI内容制作平台',
    '杭州帷幄未来科技有限公司': '零售AI解决方案公司',
    '快手-达佳互联': '短视频与直播平台',
    '礼来 Lilly': '跨国制药巨头',
    '南芥智能科技（南京）有限公司': 'AI Agent创业公司',
    '上海哔哩哔哩科技有限公司': '视频社区与内容平台',
    '上海国智技术有限公司': '数据库与大数据技术公司',
    '上海合合信息科技股份有限公司': 'AI文档与数据智能公司',
    '上海声网科技有限公司': '实时音视频云服务商',
    '上海稀宇极智科技有限公司': '下一代AI智能助理',
    '深信服科技股份有限公司': '网络安全与云计算上市公司',
    '深圳枫叶互动科技有限公司': '海外互动故事平台',
    '深圳九瓴科技有限公司': 'AI视频生成创业公司',
    '钛动科技股份有限公司': '出海营销技术平台',
    '腾讯科技（深圳）有限公司': '互联网科技巨头',
    '小满科技': '出海CRM SaaS平台',
    '行吟信息科技（上海）有限公司': '生活方式社区平台',
    '易点天下网络科技股份有限公司(西安点告网络科技有限公司）': '出海营销科技集团',
    '英矽智能科技（上海）有限公司': 'AI制药公司',
    '长量基金': '金融科技公司',
    '浙江莲花紫星智算科技有限公司': '智算AI基础设施公司',
    '中国太平洋保险(集团)股份有限公司': '保险金融集团',
    '作业帮教育科技（北京）有限公司': '在线教育平台',
}

def classify_cat(pos):
    p = pos.lower()
    if any(k in p for k in ['infra', 'gpu', '训练', '推理', '存储', '调度', 'kubernetes', 'devops',
                            '查询分析', 'flink', '实时计算', '压缩算法', '异构计算', 'pytorch',
                            '机器学习优化', '并行文件', 'maas', 'solution architect', '算力',
                            '训练框架', '推理框架', '平台全栈', 'platform']):
        return 'infra'
    if any(k in p for k in ['agent', '智能体', 'llm', '大模型', '后训练', '微调', 'sft', 'rlhf',
                            '强化学习', '应用算法', '对话', '评测', 'ai engineer', '语义',
                            'function calling', 'prompt', 'language model', '语言大模型',
                            'codebuddy', 'workbuddy', 'harness']):
        return 'agent'
    if any(k in p for k in ['推荐', '搜索', '广告', '搜广推', '召回', '排序', '算法', '多模态',
                            'nlp', '风控', '机器学习', '数据科学', '数据挖掘', 'aigc', '图像',
                            '视频生成', '音频', '语音', '视频理解', '搜索']):
        return 'algo'
    if any(k in p for k in ['多媒体', '音视频', '媒体', 'webgpu', 'webcodecs', '编解码',
                            'ffmpeg', '视频编辑', '渲染', 'opengl', '流式视频', '直播']):
        return 'media'
    if any(k in p for k in ['产品', 'pm', 'product', '产品经理', '产品总监', '商业化',
                            '营销云', '投放', '品牌', '流量', '商单', 'adx', 'sparkfly']):
        return 'product'
    if any(k in p for k in ['增长', 'growth', '出海', '海外', '运营', '优化师', '红人',
                            'kol', 'seo', 'sem', '发行', '商务', 'bd', '市场']):
        return 'growth'
    return 'exec'

cat_names = {
    'infra': '01 // AI Infra & 云计算基础设施',
    'agent': '02 // AI Agent & 大模型应用',
    'algo': '03 // 算法、搜广推与多模态',
    'media': '04 // 视频/多媒体工程',
    'product': '05 // 产品与商业化',
    'growth': '06 // 增长、出海与运营',
    'exec': '07 // 管理与战略',
}

cat_counts = {c: 0 for c in cat_names}

def clean_html(raw):
    """Strip HTML tags and return clean text"""
    if not raw or str(raw).strip() in ('None', 'null', ''):
        return []
    text = str(raw)
    # Remove <style> blocks
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    # Replace <br> with newline
    text = re.sub(r'<br\s*/?>', '\n', text)
    # Replace </li> with newline (keep content)
    text = re.sub(r'</li>', '\n', text)
    text = re.sub(r'</p>', '\n', text)
    text = re.sub(r'</div>', '\n', text)
    # Strip remaining tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    text = html_mod.unescape(text)
    # Clean up whitespace
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if line and line not in ('&nbsp;', 'null', 'None', ''):
            # Remove leading numbers/bullets
            line = re.sub(r'^\d+[\.\)、]\s*', '• ', line)
            if not line.startswith('•'):
                # Skip section headers (职位描述, 职位要求, etc.)
                if any(skip in line for skip in ['职位描述', '职位要求', '岗位职责', '任职要求', 'Qualifications',
                                                   'Responsibilities', 'About the', 'Job Description',
                                                   '职位需求', 'Main Duties', 'Requirements',
                                                   '任职要求', '岗位要求', '工作职责']):
                    continue
                line = '• ' + line
            lines.append(line)
    
    # Deduplicate and limit
    seen = set()
    unique = []
    for line in lines:
        if line not in seen and len(line) > 5:
            seen.add(line)
            unique.append(line)
    return unique[:20]

def format_items(items):
    if not items:
        return '<p style="color:#64748b;font-style:italic;">详细JD请私信联系</p>'
    return '\n'.join(f'<li>{html_mod.escape(i[2:] if i.startswith("• ") else i)}</li>' for i in items)

# Process all jobs
all_jobs = []
idx = 0
for row in ws.iter_rows(min_row=2, values_only=True):
    pos = str(row[0]).strip() if row[0] else ''
    company = str(row[1]).strip() if row[1] else ''
    loc = str(row[3]).strip() if row[3] else ''
    jd_raw = str(row[2]) if row[2] and row[2] not in ('None', 'null') else ''
    req_raw = str(row[4]) if row[4] and row[4] not in ('None', 'null') else ''
    
    if not pos or not company:
        continue
    idx += 1
    cat = classify_cat(pos)
    cat_counts[cat] += 1
    
    jd_items = clean_html(jd_raw)
    req_items = clean_html(req_raw)
    
    # If both empty, try splitting by common patterns
    if not jd_items and not req_items:
        combined = clean_html(jd_raw or req_raw or '')
        if combined:
            mid = len(combined) // 2
            jd_items = combined[:mid]
            req_items = combined[mid:]
    
    all_jobs.append({
        'id': idx,
        'pos': pos,
        'mask': company_masks.get(company, company),
        'loc': loc,
        'cat': cat,
        'jd': jd_items,
        'req': req_items,
    })

# Generate HTML
parts = []
for c in ['infra', 'agent', 'algo', 'media', 'product', 'growth', 'exec']:
    items = [j for j in all_jobs if j['cat'] == c]
    if not items:
        continue
    
    parts.append(f'''<!-- ═══ {cat_names[c]} ═══ -->
<div class="category-group" data-category="{c}">
<h2 class="category-title">{cat_names[c]}</h2>
<div class="jobs-grid">''')
    
    for j in items:
        esc_pos = html_mod.escape(j['pos'])
        esc_mask = html_mod.escape(j['mask'])
        esc_loc = html_mod.escape(j['loc'])
        jd_html = format_items(j['jd'])
        req_html = format_items(j['req'])
        jid = f"#{j['id']:03d}"
        
        parts.append(f'''<div class="job-card" data-cat="{c}">
<div class="job-header" onclick="toggleJobCard(this.parentElement)">
<span class="job-id">{jid}</span>
<h3 class="job-title">{esc_pos}</h3>
<span class="job-company-mask">{esc_mask}</span><span class="job-location">📍 {esc_loc}</span>
<p class="job-desc">{esc_pos} — {esc_mask} · {esc_loc}</p>
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
</div>''')
    
    parts.append('''</div>
</div>''')

output = '\n'.join(parts)
with open('/Users/zach.g/dev/zach-website/all_jobs.html', 'w') as f:
    f.write(output)

print(f"Jobs: {idx}")
print(f"File: {len(output)} chars")
for c in ['infra', 'agent', 'algo', 'media', 'product', 'growth', 'exec']:
    print(f"  {cat_names[c]}: {cat_counts[c]}")
