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
        self.simple_model = self.models['simple']  # Using simple model for generate citation sentences
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
                references = references + f'{j+1}.' + paper.references[i][j].reference + '\n'

            prompt = format_prompt("new_reference", paper=paper, references=references)
            new_references_response = self.complex_model.query(prompt)
            index1, index2 = -1, -1

            while True: 
                index1 = new_references_response.find('<', index1+1)
                index2 = new_references_response.find('>', index1+1)
                if index1 == -1 or index2 == -1:
                    break
                result = int(new_references_response[index1 + 1: index2])
                if result:
                    index = int(result) - 1
                    new_references.append(paper.references[i][index])
            paper.references[i] = new_references

        return paper

    def _generate_citation_sentences(self, paper: PaperBase) -> PaperBase:
        """
        Generate citation sentences from references


        Returns:
            Modified PaperBase object with updated citations
        """

        for i in range(len(paper.references)):
            section_citations = []

            for reference_paper in paper.references[i]:
                prompt = format_prompt("citation_sentence", outline=paper.outline[i], paper=reference_paper)
                citation_response = self.simple_model.query(prompt)
                # 提取<>的内容
                index1, index2 = 0, 0
                index1 = citation_response.find('<', index1)
                index2 = citation_response.find('>', index1)
                citation = citation_response[index1 + 1: index2]
                citation = citation.strip()
                if citation:
                    section_citations.append(CitationBase(citation_sentence=citation, reference=reference_paper.reference))

            paper.citation_content.append(section_citations)
        
        return paper

if __name__=="__main__":
    a = CitationGenerator()
    with open('/home/xfeng/pw0725/paper-writer/paper_writer/examples/searcher.pkl', 'rb') as f:
        paper = pickle.load(f)
    paper = a.process(paper)
    print(f"citation:\n{paper.citation_content}")
    with open('/home/xfeng/pw0725/paper-writer/paper_writer/examples/citation.pkl', 'wb') as f:
        pickle.dump(paper, f)