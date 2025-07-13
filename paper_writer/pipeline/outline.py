import json
import re
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

        outline_sections = []
        
        try:
            results = json.loads(response)
        except json.JSONDecodeError:
            # 如果直接解析失败，尝试提取JSON部分
            json_match = re.search(r'\s*\{.*\}\s*', response, re.DOTALL)
            if json_match:
                results = json.loads(json_match.group(0))
            else:
                return []

        for key, section in results.items():
            key = key.strip()
            section = section.strip()
            outline_sections.append(f"{key}:{section}")
        
        return outline_sections
    
if __name__=="__main__":
    a = OutlineGenerator()
    paper = PaperBase()
    paper.title = '移动机器人覆盖路径规划算法综述'
    paper.description = '''
**Comprehensive Description of "移动机器人覆盖路径规划算法综述"**  

**Objectives and Scope**  
This paper presents a systematic survey of coverage path planning (CPP) algorithms for mobile robots, aiming to provide a comprehensive overview of their fundamental concepts, applications, and technological developments. The scope of the paper encompasses:  
1. Defining the core principles of CPP, including its objectives (e.g., complete area coverage, obstacle avoidance, energy efficiency) and application scenarios (e.g., floor cleaning, agricultural monitoring, search-and-rescue, industrial inspection).  
2. Classifying state-of-the-art CPP algorithms into distinct categories based on their underlying methodologies, such as *cellular decomposition*, *graph-based*, *potential field*, *neural network*, and *evolutionary algorithms*.  
3. Analyzing the evolution of these algorithms, emphasizing milestones and paradigm shifts in the field.  
4. Evaluating the strengths and limitations of each algorithm class in terms of computational complexity, adaptability, scalability, and practical implementation challenges.  

**Key Contributions and Significance**  
This paper serves as a timely and structured reference for researchers and practitioners by:  
1. Offering a **taxonomy** of CPP algorithms, clarifying their relationships and applicability to different environments (static/dynamic, known/unknown).  
2. Summarizing **lessons from historical developments**, such as the transition from heuristic-based approaches to data-driven and hybrid methods.  
3. Identifying **open challenges**, including real-time adaptability, multi-robot coordination, and energy optimization, to guide future research directions.  
Its significance lies in bridging gaps between theoretical advancements and practical deployment, aiding the selection of optimal CPP strategies for specific robotic tasks.  

**Methodology**  
The study adopts a **multi-dimensional review methodology**:  
1. **Conceptual Framing**: Introduces CPP as an optimization problem, defining metrics like coverage rate, path length, and overlap minimization.  
2. **Algorithm Classification**: Categorizes existing methods into hierarchical groups (e.g., exact, heuristic, learning-based) with representative examples (e.g., boustrophedon decomposition, genetic algorithms, deep reinforcement learning).  
3. **Comparative Analysis**: Critically examines algorithms using qualitative criteria (e.g., robustness) and quantitative benchmarks (e.g., simulation results from key papers).  
4. **Trend Synthesis**: Extracts emerging patterns, such as the integration of AI/ML, and discusses their implications.  

**Expected Outcomes and Findings**  
The paper elucidates:  
1. **Trade-offs** between classical (e.g., grid-based) and modern (e.g., neural network) methods, highlighting that while classical methods excel in structured environments, data-driven approaches offer flexibility in complex settings.  
2. **Performance gaps**, such as the high computational cost of exact methods versus suboptimal but efficient heuristics.  
3. **Future trends**, including the rising role of federated learning for multi-robot CPP and the need for standardized evaluation frameworks.  

By synthesizing diverse research threads, this survey aims to accelerate innovation in CPP and foster interdisciplinary collaborations across robotics, optimization, and AI.  

---  
*Note*: The description maintains an academic tone with clear section demarcations, logical flow, and emphasis on both theoretical and practical insights. It balances breadth (coverage of methods) and depth (critical analysis) while aligning with the title’s focus on a *review/survey* paper.
    '''
    paper = a.process(paper)
    print(f"outline:\n{paper.outline}")
