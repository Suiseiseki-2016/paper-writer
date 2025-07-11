from paper_writer.pipeline.base import PipelineComponent, PaperBase
from paper_writer.utils.model import load_models
from paper_writer.utils.prompts import format_prompt

class CitationGenerator(PipelineComponent):
    """Pipeline component that generates citations for each reference."""
    
    def __init__(self):
        super().__init__("citation_generator")
        self.models = load_models()
        self.search_model = self.models['search']  # Using search model for searcher generation
        self.simple_model = self.models['simple']  # Using search model for searcher generation

    def process(self, paper: PaperBase) -> PaperBase:
        """
        Generate citations for each reference.
        
        Args:
            paper: Input PaperBase object with title, description, and references
            
        Returns:
            Modified PaperBase object with updated search results
        """
        # Generate prompt using the format_prompt function from utils.prompts
        prompt = format_prompt("citation", paper=paper)

        # Generate citations
        citations_response = self.model.query(prompt)