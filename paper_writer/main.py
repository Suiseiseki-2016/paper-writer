from paper_writer.pipeline.base import PaperBase
from paper_writer.pipeline.description import DescriptionGenerator
from paper_writer.pipeline.outline import OutlineGenerator
from paper_writer.pipeline.searcher import SearcherGenerator
from paper_writer.pipeline.citation import CitationGenerator


def main():
    print("Hello from paper-writer!")
    a = DescriptionGenerator()
    b = OutlineGenerator()
    c = SearcherGenerator()
    d = CitationGenerator()

    paper = PaperBase()
    paper.title = '太极拳对大学生生活质量与心理健康的影响研究————基于体育锻炼与校园文化的视角'
    paper.description = '探讨太极拳这一传统运动对于大学生生活质量与心理健康的促进作用。'
    paper = a.process(paper)
    paper = b.process(paper)
    paper = c.process(paper)
    paper = d.process(paper)


    print(f"description:\n{paper.description}\ncitation:\n{paper.citation_content}")

if __name__ == "__main__":
    main()
