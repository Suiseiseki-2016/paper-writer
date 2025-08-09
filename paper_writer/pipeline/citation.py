import json
import re
import pickle
from paper_writer.pipeline.base import PipelineComponent, PaperBase, ReferencePaperBase, CitationBase
from paper_writer.utils.model import load_models
from paper_writer.utils.prompts import format_prompt

class CitationGenerator(PipelineComponent):
    """Pipeline component that generates citations for each reference."""
    
    def __init__(self):
        super().__init__("citation_generator")
        self.models = load_models()
        self.search_model = self.models['search']  # Using search model for 
        self.simple_model = self.models['simple']  # Using simple model for 
        self.complex_model = self.models['complex']  # Using complex model for parse reference

    def process(self, paper: PaperBase) -> PaperBase:
        """
        Generate citations for each reference.
        
        Args:
            paper: Input PaperBase object with title, description, and references
            
        Returns:
            Modified PaperBase object with updated citations
        """
        # Select valid references
        paper = self._parse_reference(paper)

        # Generate citations
        paper = self._generate_citation_sentences(paper)
        
        print(f"citation:\n{paper.citation_content}")
        return paper

    def _parse_reference(self, paper: PaperBase) -> PaperBase:
        
        """
        从references中提取出有效的references
        """
        
        for i in range(len(paper.references)):
            new_references = []
            references = ''

            for j in range(len(paper.references[i])):
                references = references + f'{i+1}.' + paper.references[i][j].reference + '\n'
            
            prompt = format_prompt("new_reference", paper=paper, references=references)
            new_references_response = self.complex_model.query(prompt)
            response_results = self._parse_references_response(new_references_response)
            
            for index, result in response_results.items():
                # 判断是否全为正整数，如果不是，则提取其中数字部分
                if index.isdigit():
                    index_int = int(index)
                else:
                    # 提取所有数字字符
                    digits = [c for c in index if c.isdigit()]
                    index_int =  int(''.join(digits)) if digits else None
                paper.references[i][index_int - 1].reference = result
                new_references.append(paper.references[i][index_int - 1])

            paper.references[i] = new_references

        return paper

    def _parse_references_response(self, response: str) -> dict:
        """
        Parse the model response into a structured references.
        
        Args:
            response: Raw response from the model
            
        Returns:
            List of references
        """
        
        try:
            results = json.loads(response)
        except json.JSONDecodeError:
            # 如果直接解析失败，尝试提取JSON部分
            json_match = re.search(r'\s*\{.*\}\s*', response, re.DOTALL)
            if json_match:
                results = json.loads(json_match.group(0))
            else:
                return {}
            
        return results

    def _generate_citation_sentences(self, paper: PaperBase) -> PaperBase:
        """
        Generate citation sentences from references


        Returns:
            Modified PaperBase object with updated citations
        """
        #for outline, reference_papers in paper.references.items():
        for i in range(len(paper.references)):
            section_citations = []

            for reference_paper in paper.references[i]:
                prompt = format_prompt("citation_sentence", outline=paper.outline[i], paper=reference_paper)
                citation_response = self.simple_model.query(prompt)
                section_citations.append(CitationBase(citation_sentence=citation_response, reference=reference_paper.reference))

            paper.citation_content.append(section_citations)
        
        return paper

if __name__=="__main__":
    a = CitationGenerator()
    paper = PaperBase()
    paper.title = '移动机器人覆盖路径规划算法综述'
    paper.outline = ["introduction:Introduction to coverage path planning (CPP) for mobile robots, emphasizing its importance in automation and robotics.\nOverview of the objectives of CPP: complete area coverage, obstacle avoidance, energy efficiency, and adaptability.\nExplanation of the scope of the paper, including the classification of algorithms and their applications in various fields.\nStatement of the paper's key contributions: taxonomy of algorithms, historical developments, and identification of open challenges.\nBrief outline of the paper's structure and the methodology used for the review.", 'Literature Review:Historical evolution of CPP algorithms, from early heuristic-based methods to modern data-driven approaches.\nClassification of CPP algorithms into categories such as cellular decomposition, graph-based, potential field, neural network, and evolutionary algorithms.\nDiscussion of key milestones and paradigm shifts in CPP research, including the integration of AI and machine learning.\nReview of notable applications of CPP in fields like agriculture, industrial inspection, and search-and-rescue operations.\nAnalysis of gaps in existing literature, such as the lack of standardized evaluation metrics for CPP algorithms.', 'Methodology:Description of the multi-dimensional review methodology: conceptual framing, algorithm classification, comparative analysis, and trend synthesis.\nExplanation of the criteria for algorithm classification, including computational complexity, adaptability, and scalability.\nDetails on the qualitative and quantitative benchmarks used for evaluating CPP algorithms.\nOverview of the sources and selection criteria for the reviewed literature, including key papers and datasets.\nJustification for the chosen methodology and its suitability for a comprehensive survey of CPP algorithms.', 'Results and Analysis:Presentation of the taxonomy of CPP algorithms, highlighting their relationships and applicability to different environments.\nComparative analysis of algorithm performance, focusing on metrics like coverage rate, path length, and computational cost.\nIdentification of trade-offs between classical and modern CPP methods, with examples from reviewed studies.\nSummary of performance gaps and limitations, such as the high computational demands of exact methods.\nVisual or tabular representation of key findings to enhance clarity and comparability.', 'Discussion:Interpretation of the results, linking them to the objectives and scope of the paper.\nDiscussion of emerging trends in CPP, such as the use of federated learning for multi-robot coordination.\nCritical analysis of open challenges, including real-time adaptability and energy optimization, and their implications for future research.\nExploration of interdisciplinary opportunities, such as combining robotics with optimization and AI for advanced CPP solutions.\nReflection on the limitations of the review, including potential biases in literature selection and the dynamic nature of the field.', "Conclusion:Summary of the paper's key findings, including the classification and comparative analysis of CPP algorithms.\nReiteration of the significance of the survey in bridging theoretical advancements and practical applications.\nRecommendations for future research directions, such as developing standardized evaluation frameworks and exploring hybrid CPP methods.\nFinal thoughts on the potential impact of CPP advancements on the broader field of robotics and automation.\nCall to action for interdisciplinary collaboration to address the identified challenges and drive innovation in CPP."]
    path = '/home/xfeng/pw0725/paper-writer/paper_writer/examples/references_list.pkl'
    file = open(path, 'rb')
    paper.references = pickle.load(file)
    file.close()
    print(paper.references)
    paper = a.process(paper)
    print(f"citation:\n{paper.citation_content}")