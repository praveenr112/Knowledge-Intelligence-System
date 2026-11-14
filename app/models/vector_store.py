from typing import List

from config import config
from google import genai
from google.genai import types
from langchain.vectorstores import Chroma


class GeminiEmbeddings:
    def __init__(self):
        self.client = genai.Client(api_key=config.require_gemini_api_key())

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        vectors = []
        for start in range(0, len(texts), 100):
            batch = texts[start:start + 100]
            response = self.client.models.embed_content(
                model=config.GEMINI_EMBEDDING_MODEL,
                contents=batch,
                config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
            )
            if response.embeddings is None or len(response.embeddings) != len(batch):
                raise RuntimeError("Gemini returned an unexpected number of embeddings.")
            for embedding in response.embeddings:
                if embedding.values is None:
                    raise RuntimeError("Gemini returned an embedding without values.")
                vectors.append(embedding.values)
        return vectors

    def embed_query(self, text: str) -> List[float]:
        response = self.client.models.embed_content(
            model=config.GEMINI_EMBEDDING_MODEL,
            contents=text,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
        )
        if not response.embeddings or response.embeddings[0].values is None:
            raise RuntimeError("Gemini returned no embedding for the query.")
        return response.embeddings[0].values


class _ChromaEmbeddingFunction:
    def __init__(self, embeddings):
        self.embeddings = embeddings

    def __call__(self, input: List[str]) -> List[List[float]]:
        return self.embeddings.embed_documents(input)


class _EmbeddingFunctionAdapter:
    def __init__(self, embeddings):
        self.embed_documents = _ChromaEmbeddingFunction(embeddings)
        self.embeddings = embeddings

    def embed_query(self, text):
        return self.embeddings.embed_query(text)


class VectorStore:
    def __init__(self, path):
        self.path = path
        self.embeddings = _EmbeddingFunctionAdapter(GeminiEmbeddings())
        self.vector_store = Chroma(
            collection_name="knowledge_intelligence_gemini",
            persist_directory=self.path,
            embedding_function=self.embeddings
        )

    def add_documents(self, documents):
        self.vector_store.add_documents(documents)

    def similarity_search(self, query, k=4):
        return self.vector_store.similarity_search(query, k=k)
    