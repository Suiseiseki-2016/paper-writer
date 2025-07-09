import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import io
from pdfminer.high_level import extract_text

def crawl_url(url: str) -> str:
    """
    爬取指定 URL 的内容。
    - HTML: 转为 markdown
    - PDF: 解析为文本并转为 markdown
    返回 markdown 文本，若失败抛出异常。
    """
    resp = requests.get(url, timeout=10)
    try:
        resp.raise_for_status()
    except:
        return ''
    content_type = resp.headers.get('Content-Type', '').lower()
    if 'application/pdf' in content_type or url.lower().endswith('.pdf'):
        # 处理 PDF
        pdf_bytes = resp.content
        with io.BytesIO(pdf_bytes) as pdf_file:
            text = extract_text(pdf_file)
        # 简单转为 markdown（每段落加空行）
        markdown = '\n\n'.join([line.strip() for line in text.splitlines() if line.strip()])
        return markdown
    else:
        # 处理 HTML
        soup = BeautifulSoup(resp.text, 'html.parser')
        html = str(soup)
        markdown = md(html)
        return markdown