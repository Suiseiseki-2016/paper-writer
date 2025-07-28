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
            Modified PaperBase object with updated search results
        """
        # Generate prompt using the format_prompt function from utils.prompts
        paper = self._parse_reference(paper)
        paper = self._generate_citation_sentences(paper)
        

        # Generate citations
        # citations_response = self.model.query(prompt)
        return paper

    def _parse_reference(self, paper: PaperBase) -> PaperBase:

        for section, searchers in paper.references.items():
            new_references = []
            references = ''

            for i in range(len(searchers)):
                references = references + f'{i+1}.' + searchers[i].reference + '\n'
            
            prompt = format_prompt("new_reference", paper=paper, references=references)
            new_references_response = self.complex_model.query(prompt)
            response_results = self._parse_references_response(new_references_response)
            
            for index, result in response_results.items():
                searchers[int(index) - 1].reference = result
                new_references.append(searchers[int(index) - 1])

            paper.references[section] = new_references

        return paper

    def _parse_references_response(self, response: str) -> dict:
        """
        Parse the model response into a structured references.
        
        Args:
            response: Raw response from the model
            
        Returns:
            List of references
        """

        new_references = []
        
        try:
            results = json.loads(response)
        except json.JSONDecodeError:
            # 如果直接解析失败，尝试提取JSON部分
            json_match = re.search(r'\s*\{.*\}\s*', response, re.DOTALL)
            if json_match:
                results = json.loads(json_match.group(0))
            else:
                return []
            
        return results

    def _generate_citation_sentences(self, paper: PaperBase) -> PaperBase:

        for outline, reference_papers in paper.references.items():
            section_citations = []

            for reference_paper in reference_papers:
                prompt = format_prompt("citation_sentence", outline=outline, paper=reference_paper)
                citation_response = self.simple_model.query(prompt)
                section_citations.append(CitationBase(citation_sentence=citation_response, reference=reference_paper.reference))

            paper.citation_content.append(section_citations)
        
        return paper

if __name__=="__main__":
    a = CitationGenerator()
    paper = PaperBase()
    paper.title = '移动机器人覆盖路径规划算法综述'
    path = '/home/xfeng/pw0725/paper-writer/paper_writer/examples/references_dict.pkl'
    file = open(path, 'rb')
    paper.references = pickle.load(file)
    file.close()
    paper = a.process(paper)
    print(f"citation:\n{paper.citation_content}")