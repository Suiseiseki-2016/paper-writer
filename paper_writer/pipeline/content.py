import pickle
from paper_writer.pipeline.base import PipelineComponent, PaperBase
from paper_writer.utils.model import load_models
from paper_writer.utils.prompts import format_prompt

class ContentGenerator(PipelineComponent):
    """Content component that generates contents for each section."""
    
    def __init__(self):
        super().__init__("content_generator")
        self.models = load_models()
        self.complex_model = self.models['complex']  # Using complex model for parse reference
        self.reference_dict = {}  # title:[index,reference]

    def process(self, paper: PaperBase) -> PaperBase:
        
        """
        Generate content for each section.
        
        Args:
            paper: Input PaperBase object with outline and references
            
        Returns:
            Modified PaperBase object with updated content
        """
        
        paper = self._generate_section_content(paper)
        print(f"content:\n{paper.section_content}")
        paper = self._generate_paper_content(paper)
        print(f"content:\n{paper.paper_content}")

        return paper
    
    def _generate_section_content(self, paper: PaperBase) -> PaperBase:

        """
        Generate contents of the paper by sections.
        
        Args:
            paper: PaperBase object with outline and citation_content
            
        Returns:
            Modified PaperBase object with updated section_content
        """
        
        for section in range(len(paper.outline)):
            citation_str = ""

            for i in range(len(paper.references[section])):
                citation_str = citation_str + f"<citation_{i+1}> {paper.references[section][i].citation_sentence}\n"

            prompt = format_prompt("content", outline=paper.outline[section], citation_str=citation_str)
            content_response = self.complex_model.query(prompt)
            paper.section_content.append(content_response)

        return paper

    def _generate_paper_content(self, paper: PaperBase) -> PaperBase:

        """
        标签替换
        reference去重及对应序号替换
        """
        
        citation_index = 1
        paper.paper_content = paper.title + '\n'

        # 将标签替换为citation_sentence
        for i in range(len(paper.section_content)):
            content = paper.section_content[i]
            index1 = -1
            index2 = -1

            while True:
                index1 = content.find('<', index1 + 1)
                index2 = content.find('>', index1 + 1)
                if index1 == -1:
                    break

                # 防止<>中的最后一个字符不是序号而是空格
                num_index = index2-1
                while content[num_index] == ' ':
                    num_index -= 1

                reference_index = int(content[num_index]) - 1
                # 判断reference是否已经被引用过
                if paper.references[i][reference_index].title in self.reference_dict.keys():
                    cited_index = self.reference_dict[paper.references[i][reference_index].title][0]
                    content = content[0:index1] + paper.references[i][reference_index].citation_sentence[:-1] +\
                    f'[{cited_index}]。' + content[index2+1:]
                else:
                    self.reference_dict[paper.references[i][reference_index].title] =\
                    [citation_index, paper.references[i][reference_index].reference]
                    content = content[0:index1] + paper.references[i][reference_index].citation_sentence[:-1] +\
                    f'[{citation_index}]。' + content[index2+1:]
                    citation_index += 1
            paper.paper_content = paper.paper_content + content + '\n'
        
        # 生成Reference
        paper.paper_content = paper.paper_content + '参考文献\n'
        reference_list = ['' for _ in range(len(self.reference_dict))]

        for value in self.reference_dict.values():
            reference_list[value[0]-1] = value[1]

        for i in range(len(reference_list)):
            paper.paper_content = paper.paper_content + f'[{i+1}] ' + reference_list[i] + '\n'

        return paper

if __name__=="__main__":
    a = ContentGenerator()
    with open('/home/xfeng/pw0725/paper-writer/paper_writer/examples/citation.pkl', 'rb') as f:
        paper = pickle.load(f)
    paper = a.process(paper)
    with open('/home/xfeng/pw0725/paper-writer/paper_writer/examples/content.pkl', 'wb') as f:
        pickle.dump(paper, f)