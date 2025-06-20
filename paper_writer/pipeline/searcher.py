from paper_writer.pipeline.base import PipelineComponent, PaperBase
from paper_writer.utils.model import load_models
from paper_writer.utils.prompts import format_prompt
from typing import List, Dict

class SearcherGenerator(PipelineComponent):
    """Pipeline component that generates search results for each section in the outline."""
    
    def __init__(self):
        super().__init__("searcher_generator")
        self.models = load_models()
        self.model = self.models['saerch']  # Using search model for searcher generation
        
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
        section_searchers = {}
        all_searchers = []
        
        for section in paper.outline:
            # Generate search results for this specific section
            section_searchers_list = self._generate_searchers_for_section(paper, section)
            section_searchers[section] = section_searchers_list
            all_searchers.extend(section_searchers_list)
        
        # Remove duplicates while preserving order
        unique_searchers = list(dict.fromkeys(all_searchers))
        
        # Update the paper object
        paper.citations = unique_searchers
        paper.citation_content = self._generate_searcher_content(unique_searchers)
        paper.citation_sentence = self._generate_searcher_sentences(paper, section_searchers)
        
        return paper
    
    def _generate_searchers_for_section(self, paper: PaperBase, section: str) -> List[str]:
        """
        Generate search results for a specific section.
        
        Args:
            paper: PaperBase object with title and description
            section: Section name to generate search results for
            
        Returns:
            List of searcher references for the section
        """
        # Create a section-specific prompt
        section_prompt = f"""Based on the following paper title, description, and specific section, suggest relevant academic search results:\n\nTitle: {paper.title}\nDescription: {paper.description}\nSection: {section}\n\nPlease provide 3-5 key academic papers that should be cited for this specific section. \nFocus on recent and highly-cited papers relevant to this section's topic.\n\nFormat each search result as: Author(s), Title, Journal/Conference, Year"""

        # Generate search results for this section
        searchers_response = self.model.query(section_prompt)
        
        # Parse the response to extract searcher references
        searchers = self._parse_searchers_response(searchers_response)
        
        return searchers
    
    def _parse_searchers_response(self, response: str) -> List[str]:
        """
        Parse the model response to extract searcher references.
        
        Args:
            response: Raw response from the model
            
        Returns:
            List of searcher references
        """
        lines = response.strip().split('\n')
        searchers = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # Remove numbering if present
                if line[0].isdigit() and '. ' in line:
                    line = line.split('. ', 1)[1]
                # Remove bullet points
                if line.startswith('- ') or line.startswith('* '):
                    line = line[2:]
                searchers.append(line)
        
        return searchers
    
    def _generate_searcher_content(self, searchers: List[str]) -> Dict[str, str]:
        """
        Generate detailed content for each searcher.
        
        Args:
            searchers: List of searcher references
            
        Returns:
            Dictionary mapping searcher references to their detailed content
        """
        searcher_content = {}
        
        for searcher in searchers:
            content_prompt = f"""Provide a detailed summary of the following academic paper:\n\nSearcher: {searcher}\n\nPlease include:\n1. Main research question or objective\n2. Key methodology used\n3. Main findings or contributions\n4. Relevance to academic research\n\nWrite in a clear, academic style suitable for a literature review."""

            content = self.model.query(content_prompt)
            searcher_content[searcher] = content
        
        return searcher_content
    
    def _generate_searcher_sentences(self, paper: PaperBase, section_searchers: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Generate example sentences showing how to use each searcher.
        
        Args:
            paper: PaperBase object
            section_searchers: Dictionary mapping sections to their searchers
            
        Returns:
            Dictionary mapping searchers to example sentences
        """
        searcher_sentences = {}
        
        for section, searchers in section_searchers.items():
            for searcher in searchers:
                sentence_prompt = f"""Generate 2-3 example sentences showing how to properly cite the following paper in the context of this section:\n\nPaper: {searcher}\nSection: {section}\nPaper Title: {paper.title}\n\nWrite sentences that:\n1. Introduce the searcher naturally\n2. Show its relevance to the section topic\n3. Use proper academic citation style\n4. Demonstrate different ways to integrate the searcher\n\nExample format:\n- \"Previous research by [Author] (Year) has shown that...\"\n- \"Building on the work of [Author] (Year), this study...\"\n- \"Recent findings from [Author] (Year) suggest that...\" """

                sentences_response = self.model.query(sentence_prompt)
                sentences = self._parse_sentences_response(sentences_response)
                
                if searcher not in searcher_sentences:
                    searcher_sentences[searcher] = []
                searcher_sentences[searcher].extend(sentences)
        
        return searcher_sentences
    
    def _parse_sentences_response(self, response: str) -> List[str]:
        """
        Parse the model response to extract example sentences.
        
        Args:
            response: Raw response from the model
            
        Returns:
            List of example sentences
        """
        lines = response.strip().split('\n')
        sentences = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # Remove numbering and bullet points
                if line[0].isdigit() and '. ' in line:
                    line = line.split('. ', 1)[1]
                if line.startswith('- ') or line.startswith('* '):
                    line = line[2:]
                if line:  # Only add non-empty lines
                    sentences.append(line)
        
        return sentences 