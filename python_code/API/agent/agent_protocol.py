from typing import Protocol, List, Dict, Any

class AgentProtocol(Protocol):
    """
    Protocol for any Chat Client (OpenAI, Anthropic, etc.)
    """
    def get_response(self, model: str, messages: List[Dict[str, Any]]) -> Dict[str,Any]:
        ...


class EmbeddingClientProtocol(Protocol):
    """
    Protocol for any Embedding Client (HuggingFace, OpenAI, etc.)
    """
    def embed(self, text_input: str) -> List[float]:
        ...


class VectorStoreProtocol(Protocol):
    """
    Protocol for vector stores (FAISS, Chroma, Pinecone, etc.)
    """
    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]] = None) -> None:
        ...

    def similarity_search(self, query: str, k: int = 5) -> List[Any]:
        ...
