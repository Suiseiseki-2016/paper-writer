from paper_writer.pipeline.base import PipelineComponent, PaperBase
from paper_writer.utils.model import load_models
from paper_writer.utils.prompts import format_prompt

class DescriptionGenerator(PipelineComponent):
    """Pipeline component that generates a detailed description based on title and initial description."""
    
    def __init__(self):
        super().__init__("description_generator")
        self.models = load_models()
        self.model = self.models['simple']  # Using simple model for description generation
        
    def process(self, paper: PaperBase) -> PaperBase:
        """
        Generate a detailed description based on the paper's title and initial description.
        
        Args:
            paper: Input PaperBase object with title and initial description
            
        Returns:
            Modified PaperBase object with updated description
        """
        # Generate prompt using the format_prompt function from utils.prompts
        prompt = format_prompt("description", paper=paper)

        # Generate new description
        new_description = self.model.query(prompt)
        
        # Update the paper object
        paper.description = new_description
        
        return paper 