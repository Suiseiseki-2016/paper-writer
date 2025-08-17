import re
from cleantext import clean
from html import unescape
from typing import List
from paper_writer.pipeline.base import ReferencePaperBase

def clean_text(text: str) -> str:
    # 去除前后空白字符
    text = text.strip()
    
    # 替换多个连续空格为单个空格
    text = re.sub(r'\s+', ' ', text)
    
    # 去除特殊字符（保留中文、英文、数字和基本标点）
    text = re.sub(r'[^\w\u4e00-\u9fff\s,.!?，。！？、]', '', text)
    
    # 去除不可见字符（如\xa0等）
    text = ''.join(char for char in text if char.isprintable())
    
    return text

def clean_html_content(text: str) -> str:
    # 转换HTML实体（如 &nbsp; &amp; 等）
    text = unescape(text)
    
    # 去除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    
    # 去除JavaScript代码
    text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
    
    return text

def advanced_clean(text: str) -> str:
    return clean(text,
        fix_unicode=True,        # 修复Unicode字符
        to_ascii=False,          # 不转换为ASCII（保留中文）
        lower=False,             # 不转换为小写
        no_line_breaks=True,     # 去除换行符
        no_urls=True,            # 去除URL
        no_emails=True,          # 去除Email
        no_phone_numbers=True,   # 去除电话号码
        no_numbers=False,        # 保留数字
        no_digits=False,         # 保留数字
        no_currency_symbols=True,# 去除货币符号
        no_punct=False,         # 保留标点
        replace_with_punct="",   # 替换标点的字符
        replace_with_url="",
        replace_with_email="",
        replace_with_phone_number="",
        replace_with_number="",
        replace_with_digit="",
        replace_with_currency_symbol="",
        lang="en"               # 基础语言（影响某些清理规则）
    )

def clean_chinese_text(text: str) -> str:
    # 去除中文文本中的无意义字符
    text = re.sub(r'[^\u4e00-\u9fff\w\s,.!?，。！？、：；\'"“”‘’（）【】《》]', '', text)
    
    # 去除重复标点（如"你好！！"→"你好！"）
    text = re.sub(r'([,.!?，。！？])\1+', r'\1', text)
    
    # 去除空白行
    text = re.sub(r'\n\s*\n', '\n', text)
    
    return text.strip()

def full_clean_pipeline(text: str) -> str:
    # 处理HTML内容
    text = clean_html_content(text)
    
    # 处理编码和乱码问题
    text = text.encode('utf-8', errors='ignore').decode('utf-8')
    
    # 基本清理
    text = clean_text(text)
    
    # 中文特殊处理（如果是中文内容）
    text = clean_chinese_text(text)
    
    # 高级清理
    text = advanced_clean(text)
    
    return text
