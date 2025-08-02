from paper_writer.pipeline.base import PipelineComponent, PaperBase, CitationBase
from paper_writer.utils.model import load_models
from paper_writer.utils.prompts import format_prompt

class ContentGenerator(PipelineComponent):
    """Content component that generates contents for each section."""
    
    def __init__(self):
        super().__init__("content_generator")
        self.models = load_models()
        self.complex_model = self.models['complex']  # Using complex model for parse reference

    def process(self, paper: PaperBase) -> PaperBase:
        
        """
        Generate content for each section.
        
        Args:
            paper: Input PaperBase object with outline and references
            
        Returns:
            Modified PaperBase object with updated content
        """

        paper = self._generate_section_content(paper)
        

        # Generate citations
        # citations_response = self.model.query(prompt)
        print(f"content:\n{paper.section_content}")
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
            prompt = format_prompt("content", outline=paper.outline[section], citations=paper.citation_content[section])
            content_response = self.complex_model.query(prompt)
            paper.section_content.append(content_response)

        return paper

if __name__=="__main__":
    a = ContentGenerator()
    paper = PaperBase()
    paper.outline = ['introduction:1. Contextual Background: Introduction to the rising mental health challenges among university students and the need for holistic interventions. 2. Tai Chi as a Solution: Overview of Tai Chi’s historical and cultural significance, and its potential benefits for physical and mental health. 3. Study Objectives: Clear articulation of the research aims, including assessing Tai Chi’s impact on quality of life and mental health within university settings. 4. Scope and Significance: Explanation of the study’s focus on physical exercise and campus culture, and its contributions to health psychology, education policy, and cultural heritage. 5. Research Questions: Key questions guiding the study, such as how Tai Chi affects stress reduction and social connectedness among students.', 'Literature Review:1. Tai Chi and Mental Health: Review of existing studies on Tai Chi’s effects on stress, anxiety, and depression, with a focus on youth and student populations. 2. Physical Exercise and Well-being: Examination of broader literature on how physical activity, including mind-body exercises, influences quality of life and psychological health. 3. Campus Culture and Student Development: Analysis of how university environments and cultural activities contribute to student well-being and mental health. 4. Gaps in Research: Identification of underexplored areas, such as Tai Chi’s role in academic settings and its cultural relevance for modern students. 5. Theoretical Framework: Presentation of theories (e.g., biopsychosocial model) that underpin the study’s approach to understanding Tai Chi’s multifaceted benefits.', 'Methodology:1. Research Design: Description of the mixed-methods approach, combining quantitative surveys and qualitative interviews. 2. Participants and Sampling: Details on the selection of university students, including criteria for Tai Chi practitioners and control groups. 3. Data Collection Tools: Explanation of validated scales (e.g., SF-36, DASS-21) and qualitative techniques (e.g., focus groups) used to gather data. 4. Analytical Procedures: Overview of statistical methods (e.g., ANOVA, regression) for quantitative data and thematic analysis for qualitative data. 5. Contextual Factors: Discussion of how university policies, campus culture, and peer influences are incorporated into the analysis.', 'Results and Analysis:1. Quantitative Findings: Presentation of statistical results showing changes in mental health metrics (e.g., stress, anxiety) and quality of life among Tai Chi participants. 2. Qualitative Insights: Thematic analysis of student narratives highlighting personal experiences, social benefits, and challenges related to Tai Chi practice. 3. Comparative Analysis: Comparison of outcomes between Tai Chi practitioners and control groups to assess the exercise’s unique impacts. 4. Contextual Influences: Examination of how campus culture and institutional support affect Tai Chi’s adoption and effectiveness. 5. Barriers and Facilitators: Identification of factors that hinder or promote Tai Chi engagement among students.', 'Discussion:1.Interpretation of Findings: Discussion of how the results align with or diverge from existing literature on Tai Chi and student well-being. 2. Theoretical Implications: Exploration of how the study’s outcomes support or challenge theoretical frameworks related to mind-body exercise and mental health. 3. Practical Applications: Recommendations for universities on integrating Tai Chi into wellness programs and fostering a supportive campus culture. 4. Limitations: Acknowledgment of study constraints, such as sample size or cultural variability, and their implications for generalizability. 5. Future Research Directions: Suggestions for further studies, such as longitudinal designs or expanded demographic inclusion, to build on the findings.', 'Conclusion:1. Summary of Key Findings: Recapitulation of the study’s main results regarding Tai Chi’s positive effects on student mental health and quality of life. 2. Broader Implications: Reflection on the research’s significance for health psychology, educational policy, and cultural preservation. 3. Call to Action: Advocacy for institutional adoption of Tai Chi as a low-cost, culturally resonant intervention for student well-being. 4. Final Remarks: Closing thoughts on the synergy between traditional practices and modern educational needs, emphasizing the study’s contribution to holistic student development.']
    paper.citation_content = [[CitationBase(citation_sentence='太极拳作为一种解决方案，概述了太极拳的历史和文化意义，及其对身心健康潜在益处的研究目标，包括评估太极拳在大学环境中对生活质量和心理健康的影响。', reference='崔家宝, 林舰, 刘育成, 等. 大学生太极拳活动的心理健康效益: 基于ICF的系统综述[J]. 中国康复理论与实践, 2023, 29(1): 48-54.')], [CitationBase(citation_sentence='"太极拳对大学生焦虑、抑郁、睡眠质量的健康效益在ICF中主要体现在情感功能（b152）、心理运动功能（b147）、能量和驱力功能（b130）和睡眠功能（b134）。太极拳练习能改善焦虑，缓解抑郁，减轻压力。"  \n\n（译文依据：该段落直接对应提纲中“Tai Chi and Mental Health”和“Theoretical Framework”部分，具体说明太极拳通过ICF框架下的功能维度改善心理健康的机制，并涉及学生群体的抑郁、焦虑等核心议题。）', reference='崔家宝, 林舰, 刘育成, 王鹏, 曾洪发. 大学生太极拳活动的心理健康效益基于ICF的系统综述[J]. 中国康复理论与实践, 2023, 29(1): 48-54.')], [CitationBase(citation_sentence='本研究采用主题检索方式，检索Web of Science、PubMed、Medline、Scopus、中国知网、万方数据库建库至2022年11月10日公开发表的大学生参与太极拳运动及其在焦虑、抑郁、睡眠质量健康结局的相关文献，进行系统综述。  \n\n（说明：该段落直接对应提纲"数据收集工具"部分，明确说明了文献检索的数据库范围、主题及时间节点，且通过"系统综述"一词关联了混合方法中的定性分析环节。虽然原文未明确提及定量调查工具，但所选段落通过"相关文献"间接涵盖量表数据来源，是最贴近提纲要求的简洁表述。）', reference='崔家宝, 林舰, 刘育成, 王鹏, 曾洪发. 大学生太极拳活动的心理健康效益基于ICF的系统综述[J]. 中国康复理论与实践, 2023, 29(1): 48-54.')], [CitationBase(citation_sentence='太极拳对大学生焦虑、抑郁、睡眠质量的健康效益在ICF中主要体现在情感功能(b152)、心理运动功能(b147)、能量和驱力功能(b130)和睡眠功能(b134)。太极拳练习能改善焦虑，缓解抑郁，减轻压力。加入二十四式太极拳理课程的太极拳锻炼，对改善轻度和中度抑郁症患者的抑郁水平相比单一的太极拳练习效果更显著。  \n\n（注：根据提纲第一部分“定量结果”，该段同时包含数据结论与比较分析，但限于三句要求，优先提取了核心量化发现与干预效果对比的表述。）', reference='崔家宝, 林舰, 刘育成, 等. 大学生太极拳活动的心理健康效益: 基于ICF的系统综述[J]. 中国康复理论与实践, 2023, 29(1): 48-54.')], [CitationBase(citation_sentence='太极拳对大学生焦虑、抑郁、睡眠质量的健康效益在ICF中主要体现在情感功能(b152)、心理运动功能(b147)、能量和驱力功能(b130)和睡眠功能(b134)。太极拳练习能改善焦虑，缓解抑郁，减轻压力。', reference='崔家宝, 林舰, 刘育成, 等. 大学生太极拳活动的心理健康效益:基于ICF的系统综述[J]. 中国康复理论与实践, 2023, 29(1): 48-54. DOI: 10.3969/j.issn.1006-9771.2023.01.007.')], [CitationBase(citation_sentence='当前服务器错误，代码500。', reference='崔家宝, 林舰, 刘育成, 等. 大学生太极拳活动的心理健康效益: 基于ICF的系统综述[J]. 中国康复理论与实践, 2023, 29(1): 48-54. DOI: 10.3969/j.issn.1006-9771.2023.01.007.')]]
    paper = a.process(paper)
    print(paper.section_content)