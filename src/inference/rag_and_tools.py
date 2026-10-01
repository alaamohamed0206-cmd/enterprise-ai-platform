from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
import chromadb
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EnterpriseRAG:
    def __init__(self, collection_name: str = "documents"):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        self.document_store = []
        logger.info("RAG system initialized")
    
    def add_documents(
        self,
        documents: List[str],
        metadata: Optional[List[Dict]] = None
    ) -> None:
        """Add documents to RAG system"""
        for idx, doc in enumerate(documents):
            doc_id = f"doc_{datetime.now().timestamp()}_{idx}"
            embedding = self.embedding_model.encode(doc).tolist()
            
            doc_metadata = metadata[idx] if metadata else {"source": "default", "index": idx}
            
            self.collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[doc],
                metadatas=[doc_metadata]
            )
            
            self.document_store.append({
                "id": doc_id,
                "content": doc,
                "embedding": embedding,
                "metadata": doc_metadata
            })
        
        logger.info(f"Added {len(documents)} documents to RAG")
    
    def search(
        self,
        query: str,
        top_k: int = 3
    ) -> List[Dict]:
        """Search for relevant documents"""
        query_embedding = self.embedding_model.encode(query).tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        retrieved_docs = []
        for i, doc in enumerate(results['documents'][0]):
            retrieved_docs.append({
                "content": doc,
                "distance": results['distances'][0][i],
                "metadata": results['metadatas'][0][i]
            })
        
        return retrieved_docs
    
    def get_context(self, query: str, top_k: int = 3) -> str:
        """Get context for LLM from retrieved documents"""
        docs = self.search(query, top_k)
        
        context = "Retrieved Context:\n"
        for i, doc in enumerate(docs, 1):
            context += f"\n[Document {i}]\n{doc['content']}\n"
        
        return context

class EnterpriseTools:
    def __init__(self):
        self.available_tools = {
            "search": self.search_documents,
            "calculate": self.calculate,
            "summarize": self.summarize,
            "analyze": self.analyze
        }
        logger.info("Tools initialized")
    
    def search_documents(self, query: str) -> Dict:
        return {
            "tool": "search",
            "query": query,
            "results": f"Search results for: {query}",
            "timestamp": datetime.now().isoformat()
        }
    
    def calculate(self, expression: str) -> Dict:
        try:
            result = eval(expression)
            return {
                "tool": "calculate",
                "expression": expression,
                "result": result,
                "status": "success"
            }
        except Exception as e:
            return {
                "tool": "calculate",
                "expression": expression,
                "error": str(e),
                "status": "error"
            }
    
    def summarize(self, text: str) -> Dict:
        summary = text[:200] + "..." if len(text) > 200 else text
        return {
            "tool": "summarize",
            "original_length": len(text),
            "summary": summary,
            "summary_length": len(summary)
        }
    
    def analyze(self, data: Dict) -> Dict:
        return {
            "tool": "analyze",
            "data_keys": list(data.keys()),
            "data_size": len(str(data)),
            "analysis": "Data analyzed successfully"
        }
    
    def call_tool(self, tool_name: str, **kwargs) -> Dict:
        if tool_name not in self.available_tools:
            return {"error": f"Tool {tool_name} not found"}
        
        return self.available_tools[tool_name](**kwargs)
    
    def list_tools(self) -> List[str]:
        return list(self.available_tools.keys())
