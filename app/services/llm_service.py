from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from config import config

class LLMService:
    def __init__(self,vector_store):
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name=config.GEMINI_CHAT_MODEL,
            openai_api_key=config.require_gemini_api_key(),
            openai_api_base=config.GEMINI_API_BASE,
            )
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", 
            return_messages=True
            )
        
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=vector_store.vector_store.as_retriever(),
            memory=self.memory
        )

    def get_response(self, query):
        return self.chain.run({"question": query})