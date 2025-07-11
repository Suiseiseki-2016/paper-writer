from paper_writer.pipeline.base import PipelineComponent, PaperBase
from typing import Dict
import re
from paper_writer.utils.crawler import crawl_url

class CrawlerComponent(PipelineComponent):
    """Pipeline component that crawls citation URLs and stores their content."""
    def __init__(self):
        super().__init__("crawler")

    def process(self, paper: PaperBase) -> PaperBase:
        citation_content: Dict[str, str] = {}
        url_pattern = re.compile(r"https?://[\w\.-]+(?:/[\w\.-]*)*")
        for reference in paper.references:
            url_match = url_pattern.search(reference)
            if url_match:
                url = url_match.group(0)
                try:
                    raw_content = crawl_url(url)
                    processed_content = self.process_crawled_content(raw_content, url)
                    citation_content[reference] = processed_content[:50000]
                except Exception as e:
                    citation_content[reference] = f"[Failed to crawl: {e}]"
            else:
                # 不是URL，跳过
                continue
        paper.citation_content = citation_content
        return paper

    def process_crawled_content(self, content: str, url: str) -> str:
        """
        预留：对爬取到的内容进行进一步处理。
        目前直接返回原始内容。
        """
        return content
