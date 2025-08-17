import re
import pickle
from paper_writer.pipeline.base import PipelineComponent, PaperBase, ReferencePaperBase
from paper_writer.utils.model import load_models
from paper_writer.utils.prompts import format_prompt
from paper_writer.utils.crawler import crawl_url
from paper_writer.utils.text import full_clean_pipeline
from typing import List

class SearcherGenerator(PipelineComponent):
    """Pipeline component that generates search results for each section in the outline."""
    
    def __init__(self):
        super().__init__("searcher_generator")
        self.models = load_models()
        self.search_model = self.models['search']  # Using search model for searcher generation
        self.simple_model = self.models['simple']  # Using simple model for reference generation

    def process(self, paper: PaperBase) -> PaperBase:
        """
        Generate search results for each section in the outline.
        
        Args:
            paper: Input PaperBase object with title, description, and outline
            
        Returns:
            Modified PaperBase object with updated search results
        """
        if not paper.outline:
            raise ValueError("Paper must have an outline before generating search results")
        
        # Generate search results for each section
        section_searchers = []

        # Generate search results for this specific section
        for section in paper.outline:
            section_searchers_list = self._generate_searchers_for_section(paper, section)
            section_searchers.append(section_searchers_list)

        for i in range(len(section_searchers)):
            section_searchers[i] = self._crawl_urls_texts(section_searchers[i])
            section_searchers[i] = self._generate_references_from_texts(section_searchers[i])

        # Update the paper object
        paper.references = section_searchers

        print('references:\n')
        for section_referecnces in paper.references:
            for reference in section_referecnces:
                print(reference.reference)

        return paper
    
    def _generate_searchers_for_section(self, paper: PaperBase, section: str) -> List[ReferencePaperBase]:
        """
        Generate search results for a specific section.
        
        Args:
            paper: PaperBase object with title and description
            section: Section name to generate search results for
            
        Returns:
            List of searcher references for the section
        """
        # Create a section-specific prompt
        section_prompt = format_prompt("searcher", paper=paper, section=section)
        # Generate search results for this section
        searchers_response = self.search_model.query(section_prompt)
        # Parse the response to extract searcher references
        searchers = self._parse_urls_response(searchers_response)

        return searchers
    
    def _parse_urls_response(self, response: str) -> List[ReferencePaperBase]:
        """
        从response中搜索url
        
        Args:
            paper: PaperBase object
            
        Returns:
            List of ReferencePaperBase
        """
        if not response:
            return []

        url_pattern = re.compile(r"https?://[\w\.-]+(?:/[\w\.-]*)*")
        pos = 0
        urls = []

        while True:
            url_match = url_pattern.search(response[pos:])
            if url_match == None:
                break
            pos += url_match.end()
            urls.append(ReferencePaperBase(url=url_match.group()))

        return urls

    def _crawl_urls_texts(self, searchers: List[ReferencePaperBase]) -> List[ReferencePaperBase]:

        for searcher in searchers:
            text = crawl_url(searcher.url)
            text = full_clean_pipeline(text)
            searcher.text = text

        return searchers

    def _generate_references_from_texts(self, searchers: List[ReferencePaperBase]) -> List[ReferencePaperBase]:
        
        """
        Generate references from crawled texts.
        提取<>内的内容作为reference，并过滤空值
        
        Args:
            searchers
            
        Returns:
            List of references for the section
        """
        new_searchers = []

        for searcher in searchers:
            reference_prompt = format_prompt("reference", text=searcher.text)
            reference_response = self.simple_model.query(reference_prompt)
            index1, index2 = 0, 0
            index1 = reference_response.find('<', index1)
            index2 = reference_response.find('>', index1)
            reference = reference_response[index1 + 1: index2]
            if reference:
                new_searchers.append(ReferencePaperBase(url=searcher.url, text=searcher.text, reference=reference))
        return new_searchers

if __name__=="__main__":
    a = SearcherGenerator()
    with open('/home/xfeng/pw0725/paper-writer/paper_writer/examples/outline.pkl', 'rb') as f:
        paper = pickle.load(f)
    paper = a.process(paper)
    #print(f"references:\n{paper.references}")
    with open('/home/xfeng/pw0725/paper-writer/paper_writer/examples/searcher.pkl', 'wb') as f:
        pickle.dump(paper, f)