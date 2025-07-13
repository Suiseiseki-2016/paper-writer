from paper_writer.pipeline.base import PipelineComponent, PaperBase
from paper_writer.utils.model import load_models
from paper_writer.utils.prompts import format_prompt
from paper_writer.utils.crawler import crawl_url
from paper_writer.utils.cleaner import full_clean_pipeline
from typing import List, Dict
import re

class SearcherGenerator(PipelineComponent):
    """Pipeline component that generates search results for each section in the outline."""
    
    def __init__(self):
        super().__init__("searcher_generator")
        self.models = load_models()
        self.search_model = self.models['search']  # Using search model for searcher generation
        self.simple_model = self.models['simple']  # Using search model for searcher generation

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

        texts = self._crawl_urls_texts(unique_searchers)

        citations = self._generate_citations_from_texts(texts)

        # Update the paper object
        paper.citations = citations
        
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
        section_prompt = format_prompt("searcher", paper=paper, section=section)
        # Generate search results for this section
        searchers_response = self.search_model.query(section_prompt)
        # Parse the response to extract searcher references
        searchers = self._parse_urls_response(searchers_response)

        return searchers
    
    def _parse_urls_response(self, response: str) -> List[str]:
        """
        从response中搜索url
        
        Args:
            paper: PaperBase object
            
        Returns:
            List of URL
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
            urls.append(url_match.group())

        return urls

    def _crawl_urls_texts(self, searchers: List[str]) -> List[str]:
        texts = []
        for searcher in searchers:
            text = crawl_url(searcher)
            text = full_clean_pipeline(text)
            texts.append(text)

        return texts

    def _generate_citations_from_texts(self, texts: List[str]) -> List[str]:
        citations = []
        for text in texts:
            citation_prompt = format_prompt("citation", text=text)
            citation_response = self.simple_model.query(citation_prompt)
            citations.append(citation_response)

        return citations

if __name__=="__main__":
    a = SearcherGenerator()
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
*Note*: The description maintains an academic tone with clear section demarcations, logical flow, and emphasis on both theoretical and practical insights. It balances breadth (coverage of methods) and depth (critical analysis) while aligning with the title's focus on a *review/survey* paper.
    '''
    paper.outline = ["Introduction:1. Definition and importance of Coverage Path Planning (CPP) in mobile robotics.\n2. Key objectives of CPP: complete coverage, obstacle avoidance, and energy efficiency.\n3. Overview of application areas such as floor cleaning, agricultural monitoring, and industrial inspection.\n4. Purpose and scope of the survey paper: systematic classification and analysis of CPP algorithms.\n5. Outline of the paper's structure and key contributions.",'Literature Review:1. Historical evolution of CPP algorithms, from early heuristic methods to modern data-driven approaches.\n2. Classification of CPP algorithms into categories: cellular decomposition, graph-based, potential field, neural network, and evolutionary algorithms.\n3. Comparative analysis of seminal works in each category, highlighting milestones and paradigm shifts.\n4. Discussion of application-specific adaptations, such as dynamic environments or multi-robot systems.\n5. Identification of gaps in existing literature and unresolved challenges in CPP research.','Methodology:1. Conceptual framing of CPP as an optimization problem, including key metrics like coverage rate and path length.\n2. Description of the review methodology: systematic collection and categorization of CPP algorithms.\n3. Criteria for comparative analysis: computational complexity, adaptability, scalability, and practical implementation.\n4. Selection of representative algorithms from each category for in-depth evaluation.\n5. Approach to synthesizing trends and emerging patterns in CPP research.']
    paper = a.process(paper)
    print(f"citations:\n{paper.citations}")