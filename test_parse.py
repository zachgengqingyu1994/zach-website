import openpyxl
import re
from html.parser import HTMLParser

wb = openpyxl.load_workbook('/Users/zach.g/.hermes/cache/documents/doc_9863893dc942_joborder 2026-05-17 17_12_02.xlsx')
ws = wb['Sheet1']

class JDContentParser(HTMLParser):
    """Extract clean text from messy JD HTML"""
    def __init__(self):
        super().__init__()
        self.parts = []
        self.in_li = False
        self.skip_div = False
        
    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            self.in_li = True
        elif tag in ['br', 'p', 'div']:
            pass
            
    def handle_endtag(self, tag):
        if tag == 'li' and self.in_li:
            self.parts.append('')
            self.in_li = False
        elif tag in ['p', 'div']:
            pass
            
    def handle_data(self, data):
        text = data.strip()
        if text:
            if self.in_li:
                self.parts.append('• ' + text)
            else:
                self.parts.append(text)

def extract_clean_text(html_content):
    """Extract meaningful text from JD HTML"""
    if not html_content or html_content == 'None' or html_content == 'null':
        return []
    
    # Remove HTML tags but keep structure
    text = str(html_content)
    
    # Try to find list items first
    items = []
    
    # Pattern for <li>content</li>  
    li_matches = re.findall(r'<li[^>]*>(.*?)</li>', text, re.DOTALL)
    if li_matches:
        for li in li_matches:
            clean = re.sub(r'<[^>]+>', '', li).strip()
            if clean and len(clean) > 5:
                items.append('• ' + clean)
    
    # Pattern for bullet points in text
    if not items:
        # Find text between <p> or <div> tags
        text_blocks = re.findall(r'<(?:p|div)[^>]*>(.*?)</(?:p|div)>', text, re.DOTALL)
        for block in text_blocks:
            clean = re.sub(r'<[^>]+>', '', block).strip()
            if clean and len(clean) > 10:
                items.append(clean)
    
    # Split by newlines/bullets if still no structure
    if not items:
        clean = re.sub(r'<[^>]+>', '\n', text)
        for line in clean.split('\n'):
            line = line.strip()
            if line and len(line) > 10:
                items.append(line)
    
    return items[:15]  # limit to 15 items

def extract_responsibilities(text):
    """Try to extract responsibility section"""
    items = extract_clean_text(text)
    # If no clear items, return the raw cleaned text truncated
    if not items:
        clean = re.sub(r'<[^>]+>', '', str(text))
        clean = re.sub(r'\s+', ' ', clean).strip()
        if len(clean) > 20:
            items = [clean[:500]]
    return items

def extract_requirements(text):
    """Try to extract requirements section"""
    return extract_clean_text(text)

# Test with a few samples
sample_rows = []
for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True)):
    if i < 3:
        sample_rows.append(row)

for i, row in enumerate(sample_rows):
    pos = row[0]
    jd = str(row[2])[:300] if row[2] else 'N/A'
    req = str(row[4])[:300] if row[4] else 'N/A'
    print(f"=== Job {i+1}: {pos} ===")
    print(f"JD preview: {jd}")
    print(f"REQ preview: {req}")
    items_resp = extract_responsibilities(str(row[2]) if row[2] else '')
    items_req = extract_requirements(str(row[4]) if row[4] else '')
    print(f"Extracted resp items: {len(items_resp)}")
    for it in items_resp[:3]:
        print(f"  {it[:100]}")
    print(f"Extracted req items: {len(items_req)}")
    for it in items_req[:3]:
        print(f"  {it[:100]}")
    print()
