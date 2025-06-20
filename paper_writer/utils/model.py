import yaml
import os
from abc import ABC, abstractmethod
import requests
from pydantic import BaseModel as PydanticBaseModel, Field
from typing import Dict, List, Optional

class ModelConfig(PydanticBaseModel):
    model_name: str
    base_url: str
    mdoel_api_key: str

class Message(PydanticBaseModel):
    role: str
    content: str

class ChatRequest(PydanticBaseModel):
    model: str
    messages: List[Message]

class BaseModel(ABC):
    def __init__(self, model_config: ModelConfig):
        self.model_name = model_config.model_name
        self.base_url = model_config.base_url
        self.api_key = os.getenv(model_config.mdoel_api_key)
        
    @abstractmethod
    def query(self, prompt: str) -> str:
        pass

class SearchModel(BaseModel):
    def query(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        request = ChatRequest(
            model=self.model_name,
            messages=[Message(role="user", content=prompt)]
        )
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=request.model_dump()
        )
        
        response_data = response.json()
        content = response_data['choices'][0]['message']['content']
        
        # Extract citations if they exist
        citations = response_data.get('citations', [])
        if citations:
            citation_text = ', '.join(citations)
            content = f"{content}\n\nCitations: {citation_text}"
            
        return content

class SimpleModel(BaseModel):
    def query(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        request = ChatRequest(
            model=self.model_name,
            messages=[Message(role="user", content=prompt)]
        )
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=request.model_dump()
        )
        
        return response.json()['choices'][0]['message']['content']

class ComplexModel(BaseModel):
    def query(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        request = ChatRequest(
            model=self.model_name,
            messages=[Message(role="user", content=prompt)]
        )
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=request.model_dump()
        )
        
        return response.json()['choices'][0]['message']['content']

def load_models() -> Dict[str, BaseModel]:
    with open('models.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    models = {
        'search': SearchModel(ModelConfig(**config['search_modeL'])),
        'simple': SimpleModel(ModelConfig(**config['simple_modeL'])),
        'complex': ComplexModel(ModelConfig(**config['complex_model']))
    }
    
    return models
