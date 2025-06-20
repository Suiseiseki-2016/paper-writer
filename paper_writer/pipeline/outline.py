from paper_writer.pipeline.base import PipelineComponent, PaperBase
from paper_writer.utils.model import load_models
from paper_writer.utils.prompts import format_prompt

class OutlineGenerator(PipelineComponent):
    """Pipeline component that generates an outline based on title and description."""
    
    def __init__(self):
        super().__init__("outline_generator")
        self.models = load_models()
        self.model = self.models['simple']  # Using simple model for outline generation
        
    def process(self, paper: PaperBase) -> PaperBase:
        """
        Generate an outline based on the paper's title and description.
        
        Args:
            paper: Input PaperBase object with title and description
            
        Returns:
            Modified PaperBase object with updated outline
        """
        # Generate prompt using the format_prompt function from utils.prompts
        prompt = format_prompt("outline", paper=paper)

        # Generate new outline
        outline_response = self.model.query(prompt)
        
        # Parse the outline response into a list of sections
        # The model should return a structured outline that we can parse
        outline_sections = self._parse_outline_response(outline_response)
        
        # Update the paper object
        paper.outline = outline_sections
        
        return paper
    
    def _parse_outline_response(self, response: str) -> list:
        """
        Parse the model response into a structured outline.
        
        Args:
            response: Raw response from the model
            
        Returns:
            List of outline sections
        """
        # Split the response into lines and extract section titles
        lines = response.strip().split('\n')
        outline_sections = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):  # Skip empty lines and markdown headers
                # Remove numbering if present (e.g., "1. Introduction" -> "Introduction")
                if line[0].isdigit() and '. ' in line:
                    line = line.split('. ', 1)[1]
                outline_sections.append(line)
        
        return outline_sections 