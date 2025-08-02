from paper_writer.pipeline.base import PipelineComponent, PaperBase, ReferencePaperBase, CitationBase
from paper_writer.utils.model import load_models
from paper_writer.utils.prompts import format_prompt

class ContentGenerator(PipelineComponent):
    """Content component that generates contents for each section."""
    
    def __init__(self):
        super().__init__("citation_generator")
        self.models = load_models()
        self.complex_model = self.models['complex']  # Using complex model for parse reference

    def process(self, paper: PaperBase) -> PaperBase:
        """
        Generate content for each section.
        
        Args:
            paper: Input PaperBase object with outline and references
            
        Returns:
            Modified PaperBase object with updated content
        """
        # Generate prompt using the format_prompt function from utils.prompts
        paper = self._parse_reference(paper)
        print(f"new_references:\n{paper.references}")
        paper = self._generate_content(paper)
        

        # Generate citations
        # citations_response = self.model.query(prompt)
        print(f"content:\n{paper.paper_content}")
        return paper
    
    def _generate_content(self, paper: PaperBase) -> PaperBase:
        for section, citations in paper.citation_content.items():
            prompt = format_prompt("content", outline=outline, paper=reference_paper)
            content_response = self.complex_model.query(prompt)