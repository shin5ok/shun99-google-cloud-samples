from typing import Union, Dict, Optional
import vertexai
from vertexai.preview.language_models import ChatModel, InputOutputTextPair
from langchain.chains import ConversationChain

from langchain.memory import ConversationBufferMemory

class Chat:

    def __init__(self, 
                    project_id: Optional[str], 
                    model_location: Optional[str], 
                    params: Dict[str, Union[int,float]] = {}
                ):

        vertexai.init(project=project_id, location=model_location)

        parameters = {
            "temperature": 0.2,
            "max_output_tokens": 1024,
            "top_p": 0.8,
            "top_k": 40
        }
        parameters.update(params)
        from langchain.llms import VertexAI
        llm = VertexAI(**parameters)
        self.chat_model = ConversationChain(
            llm=llm,
            verbose=True,
            memory=ConversationBufferMemory()
        )

    def chat(self, req: str):
        response = self.chat_model.predict(input=req)
        return response
