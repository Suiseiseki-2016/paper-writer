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
if __name__=="__main__":
    a = DescriptionGenerator()
    paper = PaperBase()
    paper.title = '移动机器人覆盖路径规划算法综述'
    paper.description = '给出移动机器人覆盖路径规划算法的基本概念与应用背景，对目前主流的覆盖路径规划算法进行分类，讨论各类覆盖路径规划算法的'\
    '发展历程与其优缺点'
    paper = a.process(paper)
    print(f"description:\n{paper.description}")
