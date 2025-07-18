from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ReferencePaperBase(BaseModel):
    """Base class for referece content."""
    title: str = ''
    url: str = ''
    text: str = ''
    reference: str = ''

class CitationBase(BaseModel):
    """Base class for citation content."""
    citation_sentence: str = ''
    reference: str = ''

class PaperBase(BaseModel):
    """Base class for paper content."""
    
    title: str = Field(default="", description="Title of the paper")
    description: str = Field(default="", description="Brief description of the paper")
    outline: List[str] = Field(default_factory=list, description="Main outline points of the paper")
    section_outline: Dict[str, List[str]] = Field(
        default_factory=dict, 
        description="Detailed outline for each section"
    )
    references: Dict[str, List[ReferencePaperBase]] = Field(
        default_factory=dict, 
        description="Dict of section: references"
    )
    citation_content: List[List[CitationBase]] = Field(
        default_factory=list,
        description="Content of citations in each section"
    )
    paper_content: str = Field(
        default="",
        description="Complete paper content"
    )
    section_content: Dict[str, str] = Field(
        default_factory=dict,
        description="Content of each section"
    )

class PipelineComponent:
    """Base class for pipeline components that process PaperBase objects."""
    
    def __init__(self, name: str):
        """
        Initialize the pipeline component.
        
        Args:
            name: Name of the pipeline component
        """
        self.name = name
        
    def process(self, paper: PaperBase) -> PaperBase:
        """
        Process the paper content.
        
        Args:
            paper: Input PaperBase object
            
        Returns:
            Modified PaperBase object
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement process() method")
        
    def __call__(self, paper: PaperBase) -> PaperBase:
        """
        Allow the component to be called directly.
        
        Args:
            paper: Input PaperBase object
            
        Returns:
            Modified PaperBase object
        """
        return self.process(paper)
    
    

